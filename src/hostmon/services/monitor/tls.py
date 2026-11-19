
import asyncio
import ssl
from datetime import UTC, datetime

import certifi
from cryptography import x509


class TlsMonitor:
    @classmethod
    async def healthcheck(cls, url: str) -> bool:
        host = url.removeprefix("http://").removeprefix("https://").split(":")[0]
        port = 443 if url.startswith("https") else 80
        cert_info = await cls._inspect_cert(host, port)
        return bool(cert_info["trusted"])


    @classmethod
    async def _inspect_cert(cls, host: str, port: int = 443, timeout: int = 10):
        try:
            d = await asyncio.wait_for(cls._get_cert_info(host, port), timeout)
            trusted = True
            err = None

        except ssl.SSLCertVerificationError as e:
            d = await asyncio.wait_for(cls._get_cert_info(host, port, False), timeout)
            trusted = False
            err = e.verify_message

        c = x509.load_der_x509_certificate(d)
        exp = c.not_valid_after_utc
        return {
            "trusted": trusted,
            "error": err,
            "not_after": exp,
            "days_left": (exp - datetime.now(UTC)).days
        }

    @classmethod
    async def _get_cert_info(cls, host: str, port: int, verify: bool = True):
        ctx = ssl.create_default_context(cafile=certifi.where())
        if not verify:
            ctx.check_hostname, ctx.verify_mode = False, ssl.CERT_NONE
        _, w = await asyncio.open_connection(host, port, ssl=ctx)
        try:
            return w.get_extra_info("ssl_object").getpeercert(True)
        finally:
            w.close()

if __name__ == "__main__":
    print(asyncio.run(TlsMonitor().healthcheck("https://google.com")))
    print(asyncio.run(TlsMonitor().healthcheck("https://google.com:443")))
