import asyncio
import socket


class TcpMonitor:
    @classmethod
    async def healthcheck(cls, url: str, timeout: int = 1) -> bool:
        host, port = await cls._extract_host_port(url)
        try:
            with socket.create_connection((host, port), timeout):
                return True
        except OSError:
            return False

    @classmethod
    async def _extract_host_port(cls, url: str) -> tuple[str, int]:
        host = url.removeprefix("http://").removeprefix("https://")
        host = host.split(":")[0].split("/")[0]
        if len(host) == 2:
            port = int(host[1].split("/")[0])
        else:
            port = 443 if url.startswith("https") else 80

        host = socket.gethostbyname(host)

        return host, port


if __name__ == "__main__":
    print(asyncio.run(TcpMonitor().healthcheck("https://google.com/12314")))
    print(asyncio.run(TcpMonitor().healthcheck("https://google.com:443/12314")))
