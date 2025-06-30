import time

import typer
from rich.progress import track

from set_status.client import MsalClient
from set_status.config import ConfigClient, ConfigProvider

app = typer.Typer()
config_client = ConfigClient()


@app.command()
def set(
    provider: ConfigProvider = typer.Argument(
        ..., metavar="PROVIDER", help="The provider you want to configure."
    ),
):
    """Set a status configuration."""
    config = {}
    match provider:
        case ConfigProvider.slack:
            slack_token = typer.prompt("Enter slack token")
            config["token"] = slack_token
        case ConfigProvider.outlook:
            _ = MsalClient()
        case _:
            raise ValueError(
                "Unknown provider, please check: set-status configure --help"
            )

    typer.echo(f"🤖 Configuring {provider.value}...")
    for _ in track(range(10), description="Processing..."):
        # Fake processing time
        time.sleep(0.01)
    config_client.write_config(provider=provider, config=config)


@app.command()
def unset(
    provider: ConfigProvider = typer.Argument(
        ..., metavar="PROVIDER", help="The provider to remove configuration for."
    ),
):
    """Set a status configuration."""
    typer.echo(f"❌ Removing {provider.value} config...")
    config_client.remove_config(provider=provider)


@app.command()
def list(
    configured: bool = typer.Option(
        ...,
        help="List only configured providers.",
        is_flag=True,
    ),
):
    config_client.list_providers(configured=configured)
