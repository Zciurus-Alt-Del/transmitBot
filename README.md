# transmitBot
transmitBot is a simplistic wrapper class for discord.py. It is intended for cleanly integrating a super basic discord interface into other projects without having to set up a bot manually.
## Examples
### Sending a message
```python
from transmitBot import tBot

token = "insert your token here"
myChannel = "ID of a discord text channel"

myBot = tBot()
myBot.run(token)
myBot.waitUntilReady()
myBot.sendMessage("Hello World!", myChannel)
```
### Receiving messages
```python
from transmitBot import tBot

token = "insert your token here"

def printfunc(message):  # This function will be called when a new message arrives
  print(message.content)

myBot = tBot()
myBot.setOnMessageFunc(printfunc)
myBot.run(token)
```

## Limitations
transmitBot does currently only works if the discord bot is joined on exactly one server ("guild").

