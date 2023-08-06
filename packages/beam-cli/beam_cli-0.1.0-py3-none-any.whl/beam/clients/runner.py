import json
import asyncio
import shlex

from websockets import connect
from websockets.exceptions import InvalidStatusCode
from typing import Any, List
from rich.progress import Progress
from beam.commands import CommandTypes
from beam import BEAM_CONFIG, console


class Websocket:
    def __init__(self, uri: str) -> None:
        self.uri = uri

    async def __aenter__(self):
        self._conn = connect(self.uri)
        self.websocket = await self._conn.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def send(self, message):
        await self.websocket.send(message)

    async def receive(self):
        return await self.websocket.recv()


async def response_handler(
    *, progress: Any, command: str, ws: Websocket, rx_timeout: float = 0.1
):
    response = {}

    if command == CommandTypes.READY:
        try:
            response = await asyncio.wait_for(ws.receive(), timeout=rx_timeout)
            if response:
                response = json.loads(response)

        except asyncio.exceptions.TimeoutError:
            pass

    elif command == CommandTypes.RUN_COMMAND:
        exit_code = None

        while exit_code is None:
            try:
                response = await asyncio.wait_for(ws.receive(), timeout=rx_timeout)
                if response:
                    response = json.loads(response)

                stdout = response.get("stdout", "")
                exit_code = response.get("exit_code")

                if stdout is not None and stdout != "":
                    progress.print(stdout)

            except asyncio.exceptions.TimeoutError:
                pass

    return response


class RunnerClient:
    def __init__(self, *, sandbox_session_id: str) -> None:
        self.sandbox_session_id = sandbox_session_id

        # self.ws_uri = "ws://localhost:8008"
        namespace = "luke-lombardi"
        self.ws_uri = (
            f"wss://sandbox-{namespace}.slai.okteto.dev/beam/{self.sandbox_session_id}/"
        )

    async def _send_command(
        self,
        *,
        payload: Any,
    ):
        response = {}

        try:
            async with Websocket(self.ws_uri) as ws:
                await ws.send(json.dumps(payload))
                response = await response_handler(
                    progress=self.progress, command=payload.get("command"), ws=ws
                )
        except InvalidStatusCode:
            pass

        return response

    def _wait_for_ready(self) -> bool:
        ready = False
        payload = {
            "command": CommandTypes.READY,
            "token": "fake_token",
        }

        while not ready:
            response = asyncio.run(self._send_command(payload=payload))
            ready = response.get("ready") is True

            if ready:
                break

        return ready

    def _create_environment(self):
        # TODO: replace with requirements from config
        requirements = {"torch": "1.10.2"}
        # BEAM_CONFIG.packages[0]

        payload = {
            "command": CommandTypes.RUN_COMMAND,
            "token": "fake_token",
            "cmd": [
                "python",
                "-m",
                "runner.develop.create",
                f"{json.dumps(requirements)}",
            ],
            "env": {},
        }

        response = asyncio.run(self._send_command(payload=payload))
        exit_code = response.get("exit_code")

        return exit_code

    def _run_cmd(self, cmd: List[str]):
        payload = {
            "command": CommandTypes.RUN_COMMAND,
            "token": "fake_token",
            "cmd": cmd,
            "env": {},
        }

        response = asyncio.run(self._send_command(payload=payload))
        exit_code = response.get("exit_code")

        return exit_code

    def initialize(self) -> bool:
        with Progress(transient=True) as progress:
            self.progress = progress
            progress.add_task("Waiting for runner to start...", total=None)
            ready = self._wait_for_ready()

        if not ready:
            return False

        with Progress(transient=True) as progress:
            self.progress = progress
            progress.add_task("Creating environment...", total=None)
            exit_code = self._create_environment()

        return exit_code == 0

    def run(self, cmd: str) -> bool:
        cmd = shlex.split(cmd)
        exit_code = self._run_cmd(cmd=cmd)
        return exit_code == 0
