import typer
from typing_extensions import Annotated

from set_status._commands import configure, profile
from set_status.client import SlackClient
from set_status.config import ConfigProvider

app = typer.Typer()

app.add_typer(configure.app, name="configure")
app.add_typer(profile.app, name="profile")

config_mapping = {ConfigProvider.slack: SlackClient}


@app.command()
def update(
    emoji: str = typer.Argument(
        ..., metavar="EMOJI", help="Emoji to use: 🤖 or :robot:."
    ),
    description: str = typer.Argument(..., help="What are you up to?"),
    expiry: Annotated[
        str | None,
        typer.Argument(
            help="Optional, how long until the status expires. 10m, 2h, 1d etc."
        ),
    ] = None,
):
    pass


def main():
    app()
