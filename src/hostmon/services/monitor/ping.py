import asyncio
import socket
import struct


class PingMonitor:
    _packet = struct.pack('!BBHHH', 8, 0, 0x06FA, 0x1234, 1) + b'ping'
    _expected = 0x1234, 1

    @classmethod
    async def healthcheck(cls, url: str, timeout: int = 1) -> bool:
        host = await cls._normalized_host(url)
        return await asyncio.to_thread(cls._ping, host, timeout)

    @classmethod
    def _ping(cls, host: str, timeout: int = 1) -> bool:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        s.settimeout(timeout)
        s.sendto(cls._packet, (host, 0))
        try:
            data, _ = s.recvfrom(2048)
            icmp = data[20:]
            return bool(icmp[0] == 0 and struct.unpack('!HH', icmp[4:8]) == cls._expected)
        except TimeoutError:
            return False

    @classmethod
    async def _normalized_host(cls, url: str) -> str:
        host = url.removeprefix("http://").removeprefix("https://")
        host = host.split(":")[0].split("/")[0]
        return socket.gethostbyname(host)


if __name__ == "__main__":
    print(asyncio.run(PingMonitor().healthcheck("8.8.8.8")))
    print(asyncio.run(PingMonitor().healthcheck("https://google.com/12314")))
    print(asyncio.run(PingMonitor().healthcheck("https://google.com:443/12314")))
