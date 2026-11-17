import asyncio

from source import start
import uvloop


async def main():
    await start.start()


if __name__ == '__main__':
    uvloop.install()
    asyncio.run(main())
