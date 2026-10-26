"""Minimal, SSRF-safe HTTP fetch used only to download images referenced by uploaded HTML."""

from __future__ import annotations

import ipaddress
import socket
import urllib.error
import urllib.parse
import urllib.request

MAX_BYTES = 15 * 1024 * 1024
TIMEOUT = 10
MAX_REDIRECTS = 3


def _is_public_host(host: str) -> bool:
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast
                or ip.is_reserved or ip.is_unspecified):
            return False
    return bool(infos)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):  # handled manually so every hop is re-validated
        return None


def fetch(url: str) -> tuple[bytes, str] | None:
    opener = urllib.request.build_opener(_NoRedirect)
    for _ in range(MAX_REDIRECTS + 1):
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname or not _is_public_host(parsed.hostname):
            return None
        req = urllib.request.Request(url, headers={"User-Agent": "clean-paper-tts/0.1"})
        try:
            with opener.open(req, timeout=TIMEOUT) as r:
                ctype = r.headers.get("Content-Type", "").split(";")[0].strip().lower()
                data = r.read(MAX_BYTES + 1)
                if len(data) > MAX_BYTES:
                    return None
                return data, ctype
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and e.headers.get("Location"):
                url = urllib.parse.urljoin(url, e.headers["Location"])
                continue
            return None
        except Exception:
            return None
    return None
