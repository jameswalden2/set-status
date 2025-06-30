import json
from enum import Enum
from pathlib import Path

from loguru import logger

CONFIG_DIR = Path.home() / ".set_status"
CONFIG_FILENAME = "config.json"
CONFIG_FILEPATH = CONFIG_DIR / CONFIG_FILENAME


class ConfigProvider(Enum):
    slack = "slack"
    msteams = "microsoft_teams"
    outlook = "outlook"
    discord = "discord"
    gh = "github"


class ConfigClient:
    config_filepath: Path

    def __init__(self, config_dir: Path = CONFIG_DIR):
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        self.config_filepath = config_dir / CONFIG_FILENAME
        if not self.config_filepath.exists():
            with open(self.config_filepath, "+w") as f:
                json.dump({}, f, indent=4)

    def _load_config(self):
        with open(self.config_filepath) as f:
            content = json.load(f)
        return content

    def _write_config(self, content: dict):
        with open(self.config_filepath, "w") as f:
            json.dump(content, f, indent=4)

    def update_config(self, provider: ConfigProvider, config: dict):
        with open(self.config_filepath, "r") as f:
            content = json.load(f)

        content[provider.value] = config

        self._write_config(content=content)

        logger.info(f"Updated configuration for {provider.value}")

    def remove_config(self, provider: ConfigProvider):
        content = self._load_config()

        if provider.value not in content:
            logger.info("🤔 Provider not configured... no need to remove.")
            return

        content.pop(provider.value)

        self._write_config(content=content)

        logger.info(f"🚮 Removed configuration for {provider.value}")

    def read_config(self, provider: ConfigProvider) -> dict:
        content = self._load_config()
        config = content.get(provider.value)

        if config is None:
            logger.info(f"Configuration doesn't exist for {provider.value}...")
            raise ValueError(
                f"Please run: set-status configure {provider.value}, to initialize this provider."
            )

        return config

    def list_providers(self, configured: bool = False):
        content = (
            self._load_config() if configured else [x.value for x in ConfigProvider]
        )
        available_providers = ", ".join(content)
        logger.info(f"Available config providers: {available_providers}")


class SlackConfig: ...
