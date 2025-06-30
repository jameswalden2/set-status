import json
import os
import sys
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

    def __init__(self):
        Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)
        if not CONFIG_FILEPATH.exists():
            with open(CONFIG_FILEPATH, "+w") as f:
                json.dump({}, f, indent=4)

    @staticmethod
    def _load_config():
        with open(CONFIG_FILEPATH) as f:
            content = json.load(f)
        return content

    @staticmethod
    def _write_config(content: dict):
        with open(CONFIG_FILEPATH, "w") as f:
            json.dump(content, f, indent=4)

    def update_config(self, provider: ConfigProvider, config: dict):
        with open(CONFIG_FILEPATH, "r") as f:
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

    def read_config(self, provider: ConfigProvider):
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
