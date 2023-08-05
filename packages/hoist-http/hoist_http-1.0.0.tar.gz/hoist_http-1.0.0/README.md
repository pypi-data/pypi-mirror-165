# Hoist

## Developer-oriented client-server communication

-   [Documentation](https://hoist.zintensity.dev)
-   [PyPI](https://pypi.org/project/hoist-http/)

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

### Features

-   Fully type safe
-   Async ready
-   Modern API

### Installation

#### Linux/macOS

```
python3 -m pip install -U hoist-http
```

#### Windows

```
py -3 -m pip install -U hoist-http
```
