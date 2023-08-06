import time
import os

from typing import Union, Tuple
from syncthing import Syncthing, SyncthingError
from beam.processmanager import ProcessManager
from beam.constants import (
    DEFAULT_CONFIG_DIRECTORY,
    DEFAULT_SYNCTHING_LOCAL_PORT,
    DEFAULT_SYNCTHING_REMOTE_PORT,
)
from beam.clients.syncthing.templates import (
    generate_folder_template,
    generate_folder_device_template,
    generate_remote_device_template,
    generate_local_device_template,
    DEFAULT_REMOTE_DEVICE_NAME,
    DEFAULT_LOCAL_DEVICE_NAME,
    DEFAULT_REMOTE_DEVICE_PORT,
)

"""
    TODO:
    - Create ~/.beam folder (contains API key config, syncthing binary, etc)
    - Download syncthing binary into ~/.beam folder, depending on OS/distro
"""

namespace = "luke-lombardi"
API_KEY = "testmykey"  # TODO: set api key to sandbox session ID dynamically


class SyncthingClient:
    def __init__(self, sandbox_session_id: str) -> None:
        self.sandbox_session_id: str = sandbox_session_id
        self.process_manager: ProcessManager = ProcessManager()
        self.local_client: Union[Syncthing, None] = None
        self.local_config: Union[dict, None] = None
        self.remote_client: Union[Syncthing, None] = None
        self.remote_config: Union[dict, None] = None
        self.max_connection_attempts: int = 10

        self.sync_api_host = (
            f"sandbox-{namespace}.slai.okteto.dev/sync-gui/{self.sandbox_session_id}/"
        )
        self.sync_host = (
            f"sandbox-{namespace}.slai.okteto.dev:443/sync/{self.sandbox_session_id}/"
        )

        if os.path.exists(f"{DEFAULT_CONFIG_DIRECTORY}/config.xml"):
            os.remove(f"{DEFAULT_CONFIG_DIRECTORY}/config.xml")

        self._start_local_server(port=DEFAULT_SYNCTHING_LOCAL_PORT)

        local_device_id = None
        remote_device_id = None

        # Connect to local syncthing server
        self.local_client, self.local_config = self._connect_to_server(
            host="0.0.0.0", port=DEFAULT_SYNCTHING_LOCAL_PORT
        )
        for device in self.local_config["devices"]:
            if device["name"] != DEFAULT_REMOTE_DEVICE_NAME:
                local_device_id = device["deviceID"]
                break

        # Connect to remote syncthing server (on runner)
        self.remote_client, self.remote_config = self._connect_to_server(
            host=self.sync_api_host, port=None, https=True
        )

        for device in self.remote_config["devices"]:
            if device["name"] != DEFAULT_LOCAL_DEVICE_NAME:
                remote_device_id = device["deviceID"]
                break

        # Add the workspace folder to share with the runner
        self.local_config["folders"] = generate_folder_template(path=os.getcwd())
        self.local_config["folders"][0]["devices"].append(
            generate_folder_device_template(device_id=local_device_id)
        )
        self.local_config["folders"][0]["devices"].append(
            generate_folder_device_template(device_id=remote_device_id)
        )

        if len(self.local_config["devices"]) == 1:
            self.local_config["devices"].append(
                generate_remote_device_template(
                    device_name="remote",
                    device_id=remote_device_id,
                    host=self.sync_host,
                    port=443,
                )
            )

        self.local_client.system.set_config(self.local_config, and_restart=False)

        # Update remote config
        if len(self.remote_config["devices"]) == 1:
            self.remote_config["devices"].append(
                generate_local_device_template(
                    device_name="local", device_id=local_device_id
                )
            )

        # Here, we override the default listening port (which is dynamic)
        self.remote_config["options"]["reconnectionIntervalS"] = 1

        # TODO: pretty sure we can just use the default port (22000)
        # which should improve startup speed slightly
        # self.remote_config["options"]["listenAddresses"] = [
        #     # f"tcp://0.0.0.0:{DEFAULT_REMOTE_DEVICE_PORT}",
        #     "dynamic+https://relays.syncthing.net/endpoint",
        #     # f"quic://0.0.0.0:{DEFAULT_REMOTE_DEVICE_PORT}",
        # ]

        self.remote_client.system.set_config(self.remote_config, and_restart=False)

    def _start_local_server(self, port: int = DEFAULT_SYNCTHING_LOCAL_PORT):
        """Start local syncthing server"""

        self.process_manager.start(
            [
                f"{DEFAULT_CONFIG_DIRECTORY}/syncthing",
                f"--home={DEFAULT_CONFIG_DIRECTORY}/",
                f"--gui-address=0.0.0.0:{port}",
                "--no-browser",
                f"--gui-apikey={API_KEY}",
                f"--logfile={DEFAULT_CONFIG_DIRECTORY}/syncthing.log",
                "--log-max-old-files=0",
            ]
        )

    def _connect_to_server(
        self, *, host: str, port: Union[int, None], https: bool = False
    ) -> Tuple[Syncthing, dict]:
        """Connect to syncthing server and pull initial configuration"""

        client = Syncthing(API_KEY, host=host, port=port, is_https=https)

        initial_config = None
        for _ in range(self.max_connection_attempts):
            try:
                initial_config = client.system.config()
                break
            except SyncthingError:
                time.sleep(0.5)
                continue

        if not initial_config:
            raise RuntimeError("unable_to_connect_to_syncthing")

        return (client, initial_config)
