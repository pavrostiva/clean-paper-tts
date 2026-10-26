"""MHTML (web archive) -> main HTML document plus embedded resources."""

from __future__ import annotations

import email
import email.policy

from .resources import Resources


def looks_like_mhtml(data: bytes) -> bool:
    head = data[:4000].lower()
    return b"mime-version" in head and (b"multipart/related" in head or b"snapshot-content-location" in head)


def unpack_mhtml(data: bytes) -> tuple[str, str, Resources]:
    """Return (html, base_url, resources)."""
    msg = email.message_from_bytes(data, policy=email.policy.default)
    store: dict[str, tuple[bytes, str]] = {}
    html_bytes, html_charset, base = b"", "utf-8", ""
    for part in msg.walk():
        if part.is_multipart():
            continue
        ctype = part.get_content_type()
        payload = part.get_payload(decode=True) or b""
        loc = (part.get("Content-Location") or "").strip()
        cid = (part.get("Content-ID") or "").strip().strip("<>")
        if ctype == "text/html" and not html_bytes:
            html_bytes, base = payload, loc
            html_charset = part.get_content_charset() or "utf-8"
            continue
        if loc:
            store[loc] = (payload, ctype)
        if cid:
            store["cid:" + cid] = (payload, ctype)
    html = html_bytes.decode(html_charset, errors="replace")
    return html, base, Resources(base_url=base, store=store)
