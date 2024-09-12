import re
import subprocess
from dataclasses import dataclass
from typing import List, Optional

PROXY_ENABLED_PATTERN = re.compile(r"^Enabled: (.*)$", re.MULTILINE)
PROXY_SERVER_PATTERN = re.compile(r"^Server: (.*)$", re.MULTILINE)
PROXY_PORT_PATTERN = re.compile(r"^Port: (.*)$", re.MULTILINE)
LISTNETWORKSERVICEORDER_PATTERN = re.compile(r"\((\d)\) (.*)\n\(Hardware Port: (.*), Device: (.*)\)", re.MULTILINE)


@dataclass
class Networkservice:
    index: int
    networkservice: str
    hardware_port: str
    device: str


@dataclass
class ProxyInfo:
    enabled: bool
    server: str
    port: str


# base
def get_proxy(
        command: str,
        networkservice: str
) -> ProxyInfo:
    p = subprocess.run(["networksetup", f"-{command}", networkservice], stdout=subprocess.PIPE)
    stdout = p.stdout.decode('utf-8')

    enabled = PROXY_ENABLED_PATTERN.findall(stdout)[0]
    enabled = True if enabled == "Yes" else False
    server = PROXY_SERVER_PATTERN.findall(stdout)[0]
    port = PROXY_PORT_PATTERN.findall(stdout)[0]
    result = ProxyInfo(
        enabled=enabled,
        server=server,
        port=port,
    )
    return result


def set_proxy(
        command: str,
        networkservice: str,
        domain: str,
        port: str,
        username: str = "",
        password: str = "",
) -> str:
    if username and password:
        authenticated = "on"
        p = subprocess.run(
            ["networksetup", f"-{command}", networkservice, domain, port, authenticated, username, password, ],
            stdout=subprocess.PIPE)
    else:
        authenticated = "off"
        p = subprocess.run(
            ["networksetup", f"-{command}", networkservice, domain, port, authenticated, ],
            stdout=subprocess.PIPE)
    stdout = p.stdout.decode('utf-8')
    return stdout


def set_proxy_state(
        command: str,
        networkservice: str,
        enabled: bool,
) -> str:
    state = "on" if enabled else "off"
    p = subprocess.run(["networksetup", f"-{command}", networkservice, state], stdout=subprocess.PIPE)
    stdout = p.stdout.decode('utf-8')
    return stdout


# base

# region http proxy
def getwebproxy(
        networkservice: str
) -> ProxyInfo:
    """
    Display Web proxy (server, port, enabled value) info for <networkservice>.

    :param networkservice: networkservice
    :return:
    """
    return get_proxy(command="getwebproxy", networkservice=networkservice)


def setwebproxy(
        networkservice: str,
        domain: str,
        port: str,
        username: str = "",
        password: str = "",
) -> str:
    """
    Set Web proxy for <networkservice> with <domain> and <port number>.
    Turns proxy on. Specify <username> and <password> if you turn authenticated proxy support on.

    :param networkservice: networkservice, example "Wi-Fi"
    :param domain: domain
    :param port: port
    :param username: username
    :param password: password
    :return: stdout
    """
    return set_proxy(
        command="setwebproxy",
        networkservice=networkservice,
        domain=domain,
        port=port,
        username=username,
        password=password,
    )


def setwebproxystate(
        networkservice: str,
        enabled: bool,
) -> str:
    """
    Set Web proxy to either <on> or <off>.

    :param networkservice: networkservice, example "Wi-Fi"
    :param enabled:
    :return:
    """
    return set_proxy_state(command="setwebproxystate", networkservice=networkservice, enabled=enabled)


# endregion http proxy

# region https proxy
def getsecurewebproxy(
        networkservice: str
) -> ProxyInfo:
    """
    Display Secure Web proxy (server, port, enabled value) info for <networkservice>.

    :param networkservice: networkservice
    :return:
    """
    return get_proxy(command="getsecurewebproxy", networkservice=networkservice)


def setsecurewebproxy(
        networkservice: str,
        domain: str,
        port: str,
        username: str = "",
        password: str = "",
) -> str:
    """
    Set Secure Web proxy for <networkservice> with <domain> and <port number>.
    Turns proxy on. Specify <username> and <password> if you turn authenticated proxy support on.

    :param networkservice: networkservice, example "Wi-Fi"
    :param domain: domain
    :param port: port
    :param username: username
    :param password: password
    :return: stdout
    """
    return set_proxy(
        command="setsecurewebproxy",
        networkservice=networkservice,
        domain=domain,
        port=port,
        username=username,
        password=password,
    )


def setsecurewebproxystate(
        networkservice: str,
        enabled: bool,
) -> str:
    """
    Set Secure Web proxy to either <on> or <off>.

    :param networkservice: networkservice, example "Wi-Fi"
    :param enabled:
    :return:
    """
    return set_proxy_state(command="setsecurewebproxystate", networkservice=networkservice, enabled=enabled)


# endregion https proxy

# region socks proxy
def getsocksfirewallproxy(
        networkservice: str
) -> ProxyInfo:
    """
    Display SOCKS Firewall proxy (server, port, enabled value) info for <networkservice>.

    :param networkservice: networkservice
    :return:
    """
    return get_proxy(command="getsocksfirewallproxy", networkservice=networkservice)


def setsocksfirewallproxy(
        networkservice: str,
        domain: str,
        port: str,
        username: str = "",
        password: str = "",
) -> str:
    """
    Set SOCKS Firewall proxy for <networkservice> with <domain> and <port number>.
    Turns proxy on. Specify <username> and <password> if you turn authenticated proxy support on.

    :param networkservice: networkservice, example "Wi-Fi"
    :param domain: domain
    :param port: port
    :param username: username
    :param password: password
    :return: stdout
    """
    return set_proxy(
        command="setsocksfirewallproxy",
        networkservice=networkservice,
        domain=domain,
        port=port,
        username=username,
        password=password,
    )


def setsocksfirewallproxystate(
        networkservice: str,
        enabled: bool,
) -> str:
    """
    Set SOCKS Firewall proxy to either <on> or <off>.

    :param networkservice: networkservice, example "Wi-Fi"
    :param enabled:
    :return:
    """
    return set_proxy_state(command="setsocksfirewallproxystate", networkservice=networkservice, enabled=enabled)


# endregion socks proxy


def listnetworkserviceorder(
) -> List[Networkservice]:
    p = subprocess.run(["networksetup", f"-listnetworkserviceorder", ], stdout=subprocess.PIPE)
    stdout = p.stdout.decode('utf-8')
    findall_res = LISTNETWORKSERVICEORDER_PATTERN.findall(stdout)
    result = []
    for index, networkservice, hardware_port, device in findall_res:
        index = int(index)
        result_item = Networkservice(
            index=index,
            networkservice=networkservice,
            hardware_port=hardware_port,
            device=device,
        )
        result.append(result_item)
    return result
