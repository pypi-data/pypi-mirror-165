"""
NOTE: This is an edited version of `thttp` (https://github.com/sesh/thttp).
"""

from contextlib import suppress
from gzip import decompress
from json import dumps, loads
from json.decoder import JSONDecodeError
from ssl import CERT_NONE, create_default_context
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, HTTPSHandler
from urllib.request import Request as URLRequest
from urllib.request import build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Request:
    def __init__(
        self,
        url: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        data: Optional[str] = None,
        headers: dict = {},
        method: str = "GET",
        timeout: int = 5,
    ) -> None:
        method = method.upper()

        headers[
            "User-Agent"
        ] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9005 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36"

        headers = {k.lower(): v for k, v in headers.items()}

        if params:
            url += f"?{urlencode(params)}"

        if json and data:
            raise Exception("Cannot provide both json and data parameters")

        if method not in ["POST", "PATCH", "PUT"] and (json or data):
            raise Exception(
                "Request method must POST, PATCH or PUT if json or data is provided"
            )

        if json:
            headers["Content-Type"] = "application/json"

            data = dumps(json).encode("utf-8")

            headers["Content-Length"] = len(data)
        elif data:
            data = urlencode(data).encode()

            headers["Content-Length"] = len(data)

        ctx = create_default_context()

        ctx.check_hostname = False

        ctx.verify_mode = CERT_NONE

        opener = build_opener(*[HTTPSHandler(context=ctx), NoRedirect()])

        req = URLRequest(url, data=data, headers=headers, method=method)

        try:
            with opener.open(req, timeout=timeout) as resp:
                status_code, content, resp_url = (
                    resp.getcode(),
                    resp.read().decode(),
                    resp.geturl(),
                )

                headers = {k.lower(): v for k, v in list(resp.info().items())}

                if "gzip" in headers.get("content-encoding", ""):
                    content = decompress(content).decode()

                json = (
                    loads(content)
                    if "application/json" in headers.get("content-type", "").lower()
                    and content
                    else None
                )
        except HTTPError as e:
            status_code, content, resp_url = (e.code, e.read().decode(), e.geturl())

            headers = {k.lower(): v for k, v in list(e.headers.items())}

            if "gzip" in headers.get("content-encoding", ""):
                content = decompress(content).decode()

            json = (
                loads(content)
                if "application/json" in headers.get("content-type", "").lower()
                and content
                else None
            )
        except URLError:
            return False

        with suppress(JSONDecodeError):
            content = loads(content)

        (
            self.req,
            self.content,
            self.json,
            self.status_code,
            self.resp_url,
            self.headers,
        ) = (req, content, json, status_code, resp_url, headers)
