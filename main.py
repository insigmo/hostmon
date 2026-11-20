import asyncio
import logging

from hostmon import start


async def main():
    await start.start()


if __name__ == '__main__':
    # uvloop.install()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    asyncio.run(main())