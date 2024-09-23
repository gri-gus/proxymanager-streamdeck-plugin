from enum import Enum

from .networksetup import *


class ProxyTypes(Enum):
    HTTP = "http"
    HTTPS = "https"
    SOCKS = "socks"
    HTTP_HTTPS = "http(s)"


def set_proxy(
        proxy_type: ProxyTypes,
        networkservice: str,
        domain: str,
        port: str,
        username: str = "",
        password: str = "",
) -> None:
    if proxy_type is ProxyTypes.HTTP:
        res = setwebproxy(
            networkservice=networkservice,
            domain=domain,
            port=port,
            username=username,
            password=password,
        )
    elif proxy_type is ProxyTypes.HTTPS:
        res = setsecurewebproxy(
            networkservice=networkservice,
            domain=domain,
            port=port,
            username=username,
            password=password,
        )
    elif proxy_type is ProxyTypes.SOCKS:
        res = setsocksfirewallproxy(
            networkservice=networkservice,
            domain=domain,
            port=port,
            username=username,
            password=password,
        )
    elif proxy_type is ProxyTypes.HTTP_HTTPS:
        res1 = setwebproxy(
            networkservice=networkservice,
            domain=domain,
            port=port,
            username=username,
            password=password,
        )
        res2 = setsecurewebproxy(
            networkservice=networkservice,
            domain=domain,
            port=port,
            username=username,
            password=password,
        )
        res = "\n".join([res1, res2]) if res1 or res2 else ""
    else:
        raise ValueError("Bad proxy_type")
    if res:
        raise ValueError(res)


def set_proxy_state(
        proxy_type: ProxyTypes,
        networkservice: str,
        enabled: bool,
) -> None:
    if proxy_type is ProxyTypes.HTTP:
        res = setwebproxystate(
            networkservice=networkservice,
            enabled=enabled,
        )
    elif proxy_type is ProxyTypes.HTTPS:
        res = setsecurewebproxystate(
            networkservice=networkservice,
            enabled=enabled,
        )
    elif proxy_type is ProxyTypes.SOCKS:
        res = setsocksfirewallproxystate(
            networkservice=networkservice,
            enabled=enabled,
        )
    elif proxy_type is ProxyTypes.HTTP_HTTPS:
        res1 = setwebproxystate(
            networkservice=networkservice,
            enabled=enabled,
        )
        res2 = setsecurewebproxystate(
            networkservice=networkservice,
            enabled=enabled,
        )
        res = "\n".join([res1, res2]) if res1 or res2 else ""
    else:
        raise ValueError("Bad proxy_type")
    if res:
        raise ValueError(res)


def get_proxy(
        proxy_type: ProxyTypes,
        networkservice: str,
) -> ProxyInfo:
    if proxy_type is ProxyTypes.HTTP:
        res = getwebproxy(
            networkservice=networkservice,
        )
    elif proxy_type is ProxyTypes.HTTPS:
        res = getsecurewebproxy(
            networkservice=networkservice,
        )
    elif proxy_type is ProxyTypes.SOCKS:
        res = getsocksfirewallproxy(
            networkservice=networkservice,
        )
    elif proxy_type is ProxyTypes.HTTP_HTTPS:
        res1 = getwebproxy(
            networkservice=networkservice,
        )
        res2 = getsecurewebproxy(
            networkservice=networkservice,
        )
        if res1.enabled and res2.enabled and res1.server == res2.server and res1.port == res2.port:
            res = res1
        else:
            res = ProxyInfo(enabled=False, server="Unknown", port="Unknown")
    else:
        raise ValueError("Bad proxy_type")
    return res
