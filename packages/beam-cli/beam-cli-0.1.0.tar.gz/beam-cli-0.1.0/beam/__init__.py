from beam.config import BeamConfigV1
from beam import log
from rich.console import Console
from marshmallow.exceptions import ValidationError

BEAM_CONFIG: BeamConfigV1 = BeamConfigV1()
console = Console()


def load_config():
    try:
        BEAM_CONFIG.load()
    except FileNotFoundError:
        log.die(
            "No configuration file found - make sure this directory has a 'config.yaml' file present."
        )
    except ValidationError as exc:
        log.die(f"Invalid config file: {exc}")
