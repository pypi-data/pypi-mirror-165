import typer
import readline  # noqa

from operator import itemgetter
from beam import BEAM_CONFIG
from beam.decorators import with_config
from beam import console
from beam.clients.api import BeamApiClient
from beam.clients.runner import RunnerClient
from beam.clients.syncthing import SyncthingClient


@with_config
def start():
    """
    Connect to a remote sandbox environment and start working.
    """
    name = BEAM_CONFIG.name
    console.log(
        f"Starting sandbox '{name}' with compute settings: {BEAM_CONFIG.compute}"
    )

    try:
        sandbox_session = itemgetter("sandbox_session")(
            BeamApiClient.start(sandbox_name=name)
        )
    except KeyError:
        console.log(f"[red]Unable to create sandbox session: '{name}'")
        return

    runner_client = RunnerClient(sandbox_session_id=sandbox_session["id"])
    if not runner_client.initialize():
        console.log(f"[red]Unable to connect to sandbox: '{name}'")

    try:
        syncthing_client = SyncthingClient(sandbox_session_id=sandbox_session["id"])
    except RuntimeError:
        console.log("[red]Unable to connect to syncthing server.")
        return

    while True:
        cmd = typer.prompt("#")
        runner_client.run(cmd)
