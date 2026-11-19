import asyncio

import niquests


class HttpMonitor:
    async def healthcheck(self, url: str) -> bool:
        return await self._send_get(url) or await self._send_head(url)

    @classmethod
    async def _send_get(cls, url: str) -> bool:
        response_get = await niquests.aget(url)
        return response_get.status_code == 200

    @classmethod
    async def _send_head(cls, url: str) -> bool:
        response_head = await niquests.ahead(url)
        return response_head.status_code == 200


if __name__ == "__main__":
    print(asyncio.run(HttpMonitor().healthcheck("https://google.com")))
    print(asyncio.run(HttpMonitor().healthcheck("https://google.com:443")))
