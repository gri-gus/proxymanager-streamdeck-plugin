from pathlib import Path

from streamdeck_sdk_pi import *

OUTPUT_DIR = Path(__file__).parent
TEMPLATE = Path(__file__).parent / "pi_template.html"


def main():
    pi = PropertyInspector(
        action_uuid="com.ggusev.proxymanager.connectdisconnect",
        elements=[
            Select(
                uid="proxy_type",
                label="Proxy type",
                values=["http", "https", "http(s)", "socks", ],
                default_value=None,
            ),
            Textfield(
                label="Networkservice",
                uid="networkservice",
                required=True,
                placeholder="Wi-Fi",
                default_value="Wi-Fi"
            ),
            Textfield(
                label="Domain",
                uid="domain",
                required=True,
                placeholder="192.168.61.1",
            ),
            Textfield(
                label="Port",
                uid="port",
                required=True,
                pattern=r"\d{1,}",
                placeholder="1080",
            ),
            Textfield(
                label="Username",
                uid="username",
                required=False,
                placeholder="username",
            ),
            Textfield(
                label="Password",
                uid="password",
                required=False,
                placeholder="password",
            ),
        ]
    )
    pi.build(output_dir=OUTPUT_DIR, template=TEMPLATE)


if __name__ == '__main__':
    # Run to generate Property Inspector
    main()
