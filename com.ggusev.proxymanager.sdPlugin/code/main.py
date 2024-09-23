import time
from dataclasses import dataclass
from enum import IntEnum
from typing import Dict, Union

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
class MonitoringParams:
    networkservice: str
    proxy_type: ProxyTypes
    domain: str
    port: str


MONITORING_INTERVAL: float = 2
DELAY_BETWEEN_KEY_DOWN: float = 2.4
CONTEXT_TO_MONITORING_PARAMS: Dict[str, MonitoringParams] = {}
PROXY_TYPES = ["http", "https", "http(s)", "socks", ]


class ConnectDisconnectAction(Action):
    UUID = "com.ggusev.proxymanager.connectdisconnect"
    LAST_KEY_DOWN_TIME = 0

    def on_key_down(self, obj: events_received_objs.KeyDown) -> None:
        now = time.time()
        if now - self.LAST_KEY_DOWN_TIME < DELAY_BETWEEN_KEY_DOWN:
            self.show_alert(context=obj.context)
            return
        self.LAST_KEY_DOWN_TIME = now

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
            try:
                set_proxy_state(
                    proxy_type=proxy_type,
                    networkservice=networkservice,
                    enabled=False,
                )
            except Exception as err:
                logger.warning(err, exc_info=True)
                self.show_alert(context=obj.context)
                return
            self.set_state(context=obj.context, state=ConnectStates.DISABLED)
            self.show_ok(context=obj.context)
            return
        elif obj.payload.state == ConnectStates.DISABLED:
            try:
                set_proxy(
                    proxy_type=proxy_type,
                    networkservice=networkservice,
                    domain=domain,
                    port=port,
                    username=username,
                    password=password
                )
            except Exception as err:
                logger.warning(err, exc_info=True)
                self.show_alert(context=obj.context)
                return
            self.set_state(context=obj.context, state=ConnectStates.ENABLED)
            self.show_ok(context=obj.context)
            return
        self.show_alert(context=obj.context)

    def on_will_appear(self, obj: events_received_objs.WillAppear):
        self.LAST_KEY_DOWN_TIME = time.time()
        self._update_or_create_proxy_in_monitoring(obj=obj)

    def on_will_disappear(self, obj: events_received_objs.WillDisappear) -> None:
        CONTEXT_TO_MONITORING_PARAMS.pop(obj.context, None)

    def on_did_receive_settings(self, obj: events_received_objs.DidReceiveSettings) -> None:
        self._update_proxy_types_in_pi(obj=obj)
        self._update_or_create_proxy_in_monitoring(obj=obj)

    def on_property_inspector_did_appear(self, obj: events_received_objs.PropertyInspectorDidAppear) -> None:
        self.get_settings(context=obj.context)

    def _update_proxy_types_in_pi(self, obj: events_received_objs.DidReceiveSettings):
        """
        Update proxy_types when updating the plugin if they have been changed.
        """
        proxy_types, proxy_type_selected = obj.payload.settings["proxy_type"]
        if proxy_types == PROXY_TYPES:
            return
        _settings = obj.payload.settings.copy()
        _settings["proxy_type"] = [PROXY_TYPES, proxy_type_selected]
        self.set_settings(context=obj.context, payload=_settings)

    def _update_or_create_proxy_in_monitoring(
            self,
            obj: Union[
                events_received_objs.DidReceiveSettings,
                events_received_objs.WillAppear,
            ],
    ):
        networkservice = obj.payload.settings["networkservice"]
        proxy_types, proxy_type_selected = obj.payload.settings["proxy_type"]
        domain = obj.payload.settings["domain"]
        port = obj.payload.settings["port"]

        if not (networkservice and proxy_type_selected and domain and port):
            if obj.payload.state == ConnectStates.ENABLED:
                self.set_state(context=obj.context, state=ConnectStates.DISABLED)
            return
        proxy_type = ProxyTypes(proxy_type_selected)
        monitoring_params = MonitoringParams(
            networkservice=networkservice,
            proxy_type=proxy_type,
            domain=domain,
            port=port
        )
        CONTEXT_TO_MONITORING_PARAMS[obj.context] = monitoring_params

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
        context_to_monitoring_params = CONTEXT_TO_MONITORING_PARAMS.copy()
        for context, monitoring_params in context_to_monitoring_params.items():
            proxy_info = get_proxy(
                proxy_type=monitoring_params.proxy_type,
                networkservice=monitoring_params.networkservice,
            )
            if (proxy_info.enabled and proxy_info.server == monitoring_params.domain
                    and proxy_info.port == monitoring_params.port):
                self.set_state(context=context, state=ConnectStates.ENABLED)
                continue
            self.set_state(context=context, state=ConnectStates.DISABLED)


if __name__ == '__main__':
    connect_disconnect_action = ConnectDisconnectAction()
    connect_disconnect_action.run_monitoring()
    StreamDeck(
        actions=[
            connect_disconnect_action,
        ],
        log_file=settings.LOG_FILE_PATH,
        log_level=settings.LOG_LEVEL,
        log_backup_count=1,
    ).run()
