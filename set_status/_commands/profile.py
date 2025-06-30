import json
from pathlib import Path

import typer

from set_status.config import ConfigClient, ConfigProvider
from set_status.constants import CONFIG_DIR, PROFILES_FILEPATH

app = typer.Typer()
config_client = ConfigClient()


class ProfilesClient:

    def __init__(self):
        Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)
        if not PROFILES_FILEPATH.exists():
            with open(PROFILES_FILEPATH, "+w") as f:
                json.dump({}, f, indent=4)

    def add(name: str):
        pass


@app.command()
def create(
    name: ConfigProvider = typer.Argument(
        ..., metavar="NAME", help="The name of the profile."
    ),
):
    """Create a new profile."""
    client = ProfilesClient()
    client.add(name=name)
