# transmitBot
## Simple example
### Sending a message
```python
from transmitBot import tBot

token = "insert your token here"
myChannel = "ID of any discord text channel"

myBot = tBot()
myBot.run(token)
myBot.waitUntilReady()
myBot.sendMessage("Hello World!", myChannel)
```
### Receiving messages
```python
from transmitBot import tBot

token = "insert your token here"
myChannel = "ID of any discord text channel"

def printfunc(message):
  print(message.content)

myBot = tBot()
myBot.setOnMessageFunc(printfunc)
myBot.run(token)
```
