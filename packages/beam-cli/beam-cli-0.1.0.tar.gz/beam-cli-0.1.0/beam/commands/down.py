import readline  # noqa

from operator import itemgetter
from pathlib import Path
from beam.util import download_files
from beam.config import write_configuration
from beam import console
from beam.clients.api import BeamApiClient


def down(sandbox_id: str) -> None:
    """
    Download a sandbox for local development.
    """

    console.log(f"Pulling sandbox: '{sandbox_id}'")

    try:
        sandbox, download_urls = itemgetter("sandbox", "download_urls")(
            BeamApiClient.down(sandbox_id=sandbox_id)
        )
    except KeyError:
        console.log(f"[red]Unable to retrieve sandbox: '{sandbox_id}'")
        return

    name = sandbox["name"]

    try:
        Path(f"{name}").mkdir()
    except FileExistsError:
        console.log(f"[red]A folder already exists with name: '{name}'")
        return

    # Download sandbox contents
    if not download_files(download_urls, path=name):
        console.log(f"[red]Failed to download files.")
        return

    # Write configuration file
    if not write_configuration(sandbox=sandbox, path=name):
        console.log(f"[red]Failed to write configuration.")
        return

    console.log(f"Downloaded sandbox, run 'beam up' in './{name}'")
