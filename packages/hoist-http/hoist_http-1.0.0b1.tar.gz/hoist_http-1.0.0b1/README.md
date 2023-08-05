# Hoist

## Easy client-server communication

### Quick Example

```py
import hoist

server = hoist.start("test")

@server.receive("hello")
async def hello(message: hoist.Message) -> None:
    print("server got hello")
    await message.reply("hi")
```

```py
import hoist

@hoist.connect_with("test")
async def main(server: hoist.Connection):

    @server.receive("hi")
    async def hello():
        print("client got hi")

    await server.message("hello")
```
