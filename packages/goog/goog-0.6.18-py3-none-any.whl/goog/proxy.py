import re
import html
import requests


def get(
        url,  # type: str
        *,
        is_binary=None,  # type: bool
        session=None,  # type: requests.Session
        **kwargs
) -> requests.Response:
    """
    Description: Get content response of `url` via Google Translate internal proxy
    Usage: `process("http://example.com")`\\n`process("http://example.com/doc.pdf", is_binary=False)`\\n`process("https://example.com/file.zip?range=0-100", is_binary=True)`

    :param url: the HTTP Uniform Resource Locator
    :param is_binary: is target resource binary?
    :param kwargs: additional `kwargs` for `requests.Session.get`
    :return: content response
    """
    from .cdn import transform
    s = session or requests.Session()
    r = s.get(transform(url, is_binary=is_binary), **kwargs)
    setattr(r, "goog_internal_property", {
        "url": url,
        "is_binary": is_binary
    })
    return r


def process(
        response,  # type: requests.Response
) -> bytes:
    """
    Description: Process content response, reverting proxy urls done by Google Translate
    Usage: `process(get("http://example.com"))`

    :param response: response returned by `goog.proxy.get`
    :return: content response in bytes
    """
    def replace(b):
        return re.sub(
            rb'<base href=("|\').*?\1>',
            b"",
            re.sub(
                rb'<script type=("|\')text/javascript\1 src=("|\')https://www.gstatic.com.*?\2></script>',
                b"",
                re.sub(
                    rb'<meta name=("|\')robots\1 content=("|\')none\2>',
                    b"",
                    b
                )
            )
        ).replace(
            html.escape("https://translate.google.com/website?sl=auto&tl=en&anno=2&u="+origin).encode(),
            b""
        ).replace(
            html.escape("https://translate.google.com/website?sl=auto&tl=en&anno=2&u=").encode(),
            b""
        ).replace(
            (parts[0]+parts[1]+"/").encode(),
            b""
        ).replace(
            (parts[0]+parts[1]).encode(),
            b""
        ).replace(
            parts[0].encode(),
            b""
        ).replace(
            html.escape(parts[2]).encode(),
            b""
        ).replace(
            html.escape("&"+parts[2][1:]).encode(),
            b""
        )
    from .cdn import transform
    _ = getattr(response, "goog_internal_property")
    url = _["url"]
    is_binary = _["is_binary"]
    parts = transform(url, is_binary=is_binary, assemble=False)
    origin = "/".join(url.split("/")[:3])
    if not is_binary and "text/html" in response.headers["Content-Type"]:
        return replace(response.content)
    else:
        return response.content

