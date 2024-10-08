from unittest import TestCase

from macos_proxy_settings.simple_settings import (
    ProxyTypes,
    set_proxy,
    set_proxy_state,
    get_proxy,
)


class TestsSimpleSettings(TestCase):
    def test_set_proxy(self):
        res = set_proxy(
            proxy_type=ProxyTypes.SOCKS,
            networkservice="Wi-Fi",
            domain="192.168.158.9",
            port="1080",
        )
        print(res)

    def test_set_proxy_http_https(self):
        res = set_proxy(
            proxy_type=ProxyTypes.HTTP_HTTPS,
            networkservice="Wi-Fi",
            domain="192.168.158.9",
            port="1080",
        )
        print(res)

    def test_set_proxy_state_enable(self):
        res = set_proxy_state(
            proxy_type=ProxyTypes.SOCKS,
            networkservice="Wi-Fi",
            enabled=True,
        )
        print(res)

    def test_set_proxy_state_disable(self):
        res = set_proxy_state(
            proxy_type=ProxyTypes.SOCKS,
            networkservice="Wi-Fi",
            enabled=False,
        )
        print(res)

    def test_get_proxy_socks(self):
        res = get_proxy(
            proxy_type=ProxyTypes.SOCKS,
            networkservice="Wi-Fi"
        )
        print(res)

    def test_get_proxy_http(self):
        res = get_proxy(
            proxy_type=ProxyTypes.HTTP,
            networkservice="Wi-Fi"
        )
        print(res)

    def test_get_proxy_https(self):
        res = get_proxy(
            proxy_type=ProxyTypes.HTTPS,
            networkservice="Wi-Fi"
        )
        print(res)

    def test_get_proxy_http_https(self):
        res = get_proxy(
            proxy_type=ProxyTypes.HTTP_HTTPS,
            networkservice="Wi-Fi"
        )
        print(res)
