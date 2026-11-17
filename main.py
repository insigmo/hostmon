import asyncio

from hostmon import start


async def main():
    await start.start()


if __name__ == '__main__':
    # uvloop.install()
    asyncio.run(main())
