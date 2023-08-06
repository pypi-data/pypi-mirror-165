import typer
import readline  # noqa

from beam import BEAM_CONFIG
from beam.decorators import with_config
from beam import console
from beam.clients.api import BeamApiClient
from beam.clients.runner import RunnerClient


@with_config
def up():
    """
    Push local changes to remote sandbox store.
    """

    console.log(f"Loading sandbox with compute settings: {BEAM_CONFIG.compute}")
