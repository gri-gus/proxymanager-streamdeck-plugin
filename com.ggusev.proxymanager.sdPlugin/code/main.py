import time
from dataclasses import dataclass
from enum import IntEnum
from typing import Dict

from streamdeck_sdk import (
    StreamDeck,
    Action,
    events_received_objs,
    in_separate_thread,
    log_errors,
    logger,
)

import settings
from macos_proxy_settings.simple_settings import (
    ProxyTypes,
    set_proxy,
    get_proxy,
    set_proxy_state,
)


class ConnectStates(IntEnum):
    DISABLED = 0
    ENABLED = 1


@dataclass
class ProxySettings:
    networkservice: str
    proxy_type: ProxyTypes
    domain: str
    port: str


MONITORING_INTERVAL: float = 2
DELAY_BETWEEN_KEY_DOWN: float = 2.4
CONTEXT_TO_PROXY_SETTINGS: Dict[str, ProxySettings] = {}


class ConnectDisconnectAction(Action):
    UUID = "com.ggusev.proxymanager.connectdisconnect"
    LAST_KEY_DOWN_TIME = 0

    def on_key_down(self, obj: events_received_objs.KeyDown) -> None:
        if time.time() - self.LAST_KEY_DOWN_TIME < DELAY_BETWEEN_KEY_DOWN:
            self.show_alert(context=obj.context)
            return
        self.LAST_KEY_DOWN_TIME = time.time()

        networkservice = obj.payload.settings["networkservice"]
        proxy_types, proxy_type_selected = obj.payload.settings["proxy_type"]
        domain = obj.payload.settings["domain"]
        port = obj.payload.settings["port"]
        username = obj.payload.settings["username"]
        password = obj.payload.settings["password"]

        if not (networkservice and proxy_type_selected and domain and port):
            self.show_alert(context=obj.context)
            return
        proxy_type = ProxyTypes(proxy_type_selected)

        if obj.payload.state == ConnectStates.ENABLED:
            set_proxy_state_error = set_proxy_state(
                proxy_type=proxy_type,
                networkservice=networkservice,
                enabled=False,
            )
            if set_proxy_state_error:
                self.show_alert(context=obj.context)
                return
            self.set_state(context=obj.context, state=ConnectStates.DISABLED)
            self.show_ok(context=obj.context)
            return
        elif obj.payload.state == ConnectStates.DISABLED:
            set_proxy_error = set_proxy(
                proxy_type=proxy_type,
                networkservice=networkservice,
                domain=domain,
                port=port,
                username=username,
                password=password
            )
            if set_proxy_error:
                self.show_alert(context=obj.context)
                return
            self.set_state(context=obj.context, state=ConnectStates.ENABLED)
            self.show_ok(context=obj.context)
            return
        self.show_alert(context=obj.context)

    @log_errors
    def on_will_appear(self, obj: events_received_objs.WillAppear):
        networkservice = obj.payload.settings["networkservice"]
        proxy_types, proxy_type_selected = obj.payload.settings["proxy_type"]
        domain = obj.payload.settings["domain"]
        port = obj.payload.settings["port"]

        if not (networkservice and proxy_type_selected and domain and port):
            self.set_state(context=obj.context, state=ConnectStates.DISABLED)
            return
        proxy_type = ProxyTypes(proxy_type_selected)
        proxy_settings = ProxySettings(
            networkservice=networkservice,
            proxy_type=proxy_type,
            domain=domain,
            port=port
        )
        CONTEXT_TO_PROXY_SETTINGS[obj.context] = proxy_settings

    @log_errors
    def on_will_disappear(self, obj: events_received_objs.WillDisappear) -> None:
        CONTEXT_TO_PROXY_SETTINGS.pop(obj.context, None)

    @in_separate_thread(daemon=True)
    @log_errors
    def run_monitoring(self):
        while True:
            time.sleep(MONITORING_INTERVAL)
            try:
                self.monitoring_iteration()
            except Exception as err:
                logger.exception(err)

    def monitoring_iteration(self):
        for context, proxy_settings in CONTEXT_TO_PROXY_SETTINGS.items():
            proxy_info = get_proxy(proxy_type=proxy_settings.proxy_type, networkservice=proxy_settings.networkservice)
            if (proxy_info.enabled and proxy_info.server == proxy_settings.domain
                    and proxy_info.port == proxy_settings.port):
                self.set_state(context=context, state=ConnectStates.ENABLED)
                continue
            self.set_state(context=context, state=ConnectStates.DISABLED)


connect_disconnect_action = ConnectDisconnectAction()
connect_disconnect_action.run_monitoring()

if __name__ == '__main__':
    StreamDeck(
        actions=[
            connect_disconnect_action,
        ],
        log_file=settings.LOG_FILE_PATH,
        log_level=settings.LOG_LEVEL,
        log_backup_count=1,
    ).run()
