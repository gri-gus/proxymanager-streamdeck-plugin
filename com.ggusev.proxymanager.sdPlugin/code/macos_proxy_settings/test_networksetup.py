from unittest import TestCase

from macos_proxy_settings.networksetup import *


class TestsNetworkSetup(TestCase):
    def test_getsocksfirewallproxy(self):
        res = getsocksfirewallproxy(networkservice="Wi-Fi")
        print(res)

    def test_setsocksfirewallproxy(self):
        res = setsocksfirewallproxy(
            networkservice="Wi-Fi",
            domain="192.168.158.9",
            port="1080",
            username="123",
            password="123",
        )
        print(res)

    def test_setsocksfirewallproxy_w(self):
        res = setsocksfirewallproxy(
            networkservice="Wi-Fi",
            domain="192.168.158.9",
            port="1080",
        )
        print(res)

    def test_setsocksfirewallproxystate(self):
        res = setsocksfirewallproxystate(networkservice="Wi-Fi", enabled=False)
        print(res)

    def test_getwebproxy(self):
        res = getwebproxy(networkservice="Wi-Fi")
        print(res)

    def test_setwebproxy(self):
        res = setwebproxy(
            networkservice="Wi-Fi",
            domain="192.168.158.9",
            port="1080",
            username="123",
            password="123",
        )
        print(res)

    def test_setwebproxystate(self):
        res = setwebproxystate(networkservice="Wi-Fi", enabled=False)
        print(res)

    def test_getsecurewebproxy(self):
        res = getsecurewebproxy(networkservice="Wi-Fi")
        print(res)

    def test_setsecurewebproxy(self):
        res = setsecurewebproxy(
            networkservice="Wi-Fi",
            domain="192.168.158.9",
            port="1080",
            username="123",
            password="123",
        )
        print(res)

    def test_setsecurewebproxystate(self):
        res = setsecurewebproxystate(networkservice="Wi-Fi", enabled=False)
        print(res)

    def test_listnetworkserviceorder(self):
        res = listnetworkserviceorder()
        print(res)
