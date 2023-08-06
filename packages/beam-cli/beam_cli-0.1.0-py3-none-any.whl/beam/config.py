import yaml

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Any
from dataclasses_json import DataClassJsonMixin
from yamldataclassconfig.config import YamlDataClassConfig
from yamldataclassconfig import create_file_path_field
from beam import constants


class Runtimes:
    PYTHON_38 = "python3.8"


@dataclass
class ComputeConfig(DataClassJsonMixin):
    gpu: int
    cpu: int
    mem: str


@dataclass
class BeamConfigV1(YamlDataClassConfig):
    FILE_PATH: Path = create_file_path_field(
        Path(__file__).parent.cwd() / "config.yaml"
    )
    name: Optional[str] = None
    compute: ComputeConfig = field(default=ComputeConfig(gpu=0, cpu=4, mem="8Gi"))
    apt: List[str] = field(default_factory=lambda: [])
    runtime: str = Runtimes.PYTHON_38
    packages: List[str] = field(default_factory=lambda: [])


def write_configuration(*, sandbox: Any, path: str) -> bool:
    compute_settings = sandbox.get("compute_settings", {})
    apt = sandbox.get("apt", [])  # TODO: add in system level dependencies
    packages = sandbox.get("requirements", {})
    runtime = sandbox.get("python_runtime", Runtimes.PYTHON_38).lower()

    cpu = compute_settings.get("cpus", constants.DEFAULT_CONFIG_CPU)
    memory = compute_settings.get("gpus", constants.DEFAULT_CONFIG_MEMORY)
    gpu = compute_settings.get("gpus", constants.DEFAULT_CONFIG_GPU)

    config = {
        "name": sandbox["name"],
        "compute": {
            "cpu": cpu,
            "mem": memory,
            "gpu": gpu,
        },
        "apt": apt,
        "runtime": runtime,
        "packages": [f"{req}=={version}" for req, version in packages.items()],
    }

    with open(f"{path}/config.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    return True
