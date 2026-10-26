from __future__ import annotations

import base64
import mimetypes
import urllib.parse

from .. import net


class Resources:
    """Resolves ``src`` attributes to image bytes (embedded MHTML parts, data URIs, or the web)."""

    def __init__(self, base_url: str = "", store: dict[str, tuple[bytes, str]] | None = None,
                 fetch_remote: bool = False, max_fetches: int = 80):
        self.base_url = base_url
        self.store = store or {}
        self.fetch_remote = fetch_remote
        self.remaining = max_fetches
        self._cache: dict[str, tuple[bytes, str] | None] = {}

    def get(self, src: str | None) -> tuple[bytes, str] | None:
        if not src:
            return None
        src = src.strip()
        if src in self._cache:
            return self._cache[src]
        res = self._resolve(src)
        self._cache[src] = res
        return res

    def _resolve(self, src: str) -> tuple[bytes, str] | None:
        if src.startswith("data:"):
            try:
                head, payload = src.split(",", 1)
                mime = head[5:].split(";")[0] or "application/octet-stream"
                data = base64.b64decode(payload) if ";base64" in head else urllib.parse.unquote_to_bytes(payload)
                return data, mime
            except Exception:
                return None
        if src.startswith("cid:"):
            return self.store.get(src)
        url = urllib.parse.urljoin(self.base_url, src) if self.base_url else src
        for key in (url, url.split("#")[0], url.split("?")[0], src):
            if key in self.store:
                return self.store[key]
        if self.fetch_remote and self.remaining > 0 and url.startswith(("http://", "https://")):
            self.remaining -= 1
            got = net.fetch(url)
            if got:
                data, ctype = got
                return data, ctype or mimetypes.guess_type(url)[0] or ""
        return None
