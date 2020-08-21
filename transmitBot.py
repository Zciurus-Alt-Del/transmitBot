import discord
from discord.ext import tasks
import asyncio
import threading
import queue
import inspect
class tBot:
    def __init__(self):
        self._discord_send_msg_queue = queue.Queue()
        self._botIsRunning: bool = False

        # Listener
        self._onMsgFunc = None
        self.onlyTheseChannelIDs = []  # public!

    def _runDiscordBot(self, q: queue.Queue, secret: str):
        """
        Runs the discord Bot (private function). This function should be called in a seperate thread as it will not return.
        :param q: Inbound queue for messages to be sent. Queue packets must be of the format (message, channel id)
        :param secret: The bots secret token
        """

        # thread stuff
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # actual bot
        client = discord.Client()
        self.mainGuild = None
        self.discord_client = client

        @client.event
        async def on_ready():
            print("Bot logged in successfully")
            num_servers = len(client.guilds)
            if num_servers < 1:
                raise LookupError(f'This bot is currently not joined on a server. It will only work if it is joined on one server.')
            elif num_servers > 1:
                raise LookupError(f'This bot is currently joined on {num_servers} servers. It will only work if it is joined on one server only.')
            else:
                self.mainGuild = client.guilds[0]

            self._botIsRunning = True
            sendqueueChecker.start()

        @client.event
        async def on_message(message):
            author = message.author.id
            me = client.user.id
            channel = message.channel.id
            if author != me:
                if ((self.onlyTheseChannelIDs and channel in self.onlyTheseChannelIDs) or not self.onlyTheseChannelIDs) and self._onMsgFunc:
                    func = threading.Thread(target=self._onMsgFunc, args=[message])
                    func.start()
                    #self._onMsgFunc()


        @tasks.loop(seconds=0.1)
        async def sendqueueChecker():
            if not self.mainGuild:
                return

            try:
                msg, channelID = q.get(timeout=0)
            except queue.Empty:
                return

            channel = self.mainGuild.get_channel(channelID)
            if channel:
                await channel.send(msg)

        client.run(secret)

    def run(self, secret):
        """
        Public function for starting the discord bot.
        :param secret: The bots secret token
        :return:
        """
        self.discord_thread = threading.Thread(target=self._runDiscordBot, args=[self._discord_send_msg_queue, secret])
        self.discord_thread.start()

    def waitUntilReady(self):
        """
        Idles until the Bot has successfully started. This will "pause" your current thread.
        :return:
        """

        while True:
            if self._botIsRunning:
                break

    def sendMessage(self, message: str, channelID: int):
        """
        Makes the bot send the message to the given channelID
        :param message:
        :param channelID:
        :return:
        """
        if self.botIsRunning:
            self._discord_send_msg_queue.put((message, channelID))
        else:
            print('The Bot is not running. Start it with .run()')

    # Getter and Setter functions

    def setOnMessageFunc(self, function):
        """
        Updates the function to be called when a new message comes in. Function must have exactly one parameter.
        When a new message arives, the given function will be called in a new thread with the message object as its parameter.

        Unless `onlyTheseChannelIDs` contains ids, this will react to EVERY message, including PMs.
        :param function:
        """
        if function is None:
            self._onMsgFunc = None
            return

        argl = len(inspect.getfullargspec(function).args)
        if argl == 1:
            self._onMsgFunc = function
        else:
            raise AttributeError('The onMsgFunc must have only one paramter, but the given function has ' + str(argl) + ' parameters')

    def botIsRunning(self) -> bool:
        return self._botIsRunning

