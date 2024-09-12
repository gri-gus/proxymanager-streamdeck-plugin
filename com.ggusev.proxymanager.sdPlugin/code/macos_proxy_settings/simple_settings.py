from enum import Enum

from .networksetup import *


class ProxyTypes(Enum):
    HTTP = "http"
    HTTPS = "https"
    SOCKS = "socks"


def set_proxy(
        proxy_type: ProxyTypes,
        networkservice: str,
        domain: str,
        port: str,
        username: str = "",
        password: str = "",
):
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
    else:
        raise ValueError("Bad proxy_type")
    return res
