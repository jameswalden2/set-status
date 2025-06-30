import os
from pathlib import Path

import httpx
from loguru import logger
from msal import PublicClientApplication
from msal_extensions import (
    FilePersistence,
    PersistedTokenCache,
    build_encrypted_persistence,
)
from msgraph import GraphServiceClient
from msgraph.generated.models.automatic_replies_setting import AutomaticRepliesSetting
from msgraph.generated.models.automatic_replies_status import AutomaticRepliesStatus
from msgraph.generated.models.date_time_time_zone import DateTimeTimeZone
from msgraph.generated.models.mailbox_settings import MailboxSettings

from set_status.constants import CONFIG_DIR

CLIENT_ID = os.environ["AZURE_AD_CLIENT_ID"]
TENANT_ID = os.environ["AZURE_AD_TENANT_ID"]


class BaseClient:
    base_url: str
    headers: dict[str, str]
    client: httpx.AsyncClient

    def __init__(self):
        self.client = httpx.AsyncClient(headers=self.headers)

    async def post(
        self,
        path: str,
        json: dict,
        params: dict | None = None,
        body: dict | None = None,
    ):
        logger.info(f"Making POST request to {self.base_url}/{path}")
        response = await self.client.request(
            method="POST",
            url=f"{self.base_url}/{path}",
            json=json,
            params=params,
            data=body,
        )
        return response.json()

    async def set_status(
        self, status: str, emoji: str, expires: int | None = None
    ) -> str: ...

    def configure(): ...


class SlackClient(BaseClient):
    # base_url: str = "https://slack.com"
    base_url: str = "https://api.restful-api.dev"

    def __init__(self, config: dict):
        self.headers = {
            "Content-type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {config["token"]}",
        }
        super().__init__()

    async def set_status(
        self, status: str, emoji: str, expires: int | None = None
    ) -> str:
        logger.info("📱 Setting Slack status...")
        response = await self.post(
            path="objects",
            json={
                "status_text": status,
                "status_emoji": emoji,
                "status_expiration": 0,
            },
        )
        return response.json()

    def configure(): ...


class MSTeamsClient(BaseClient):
    base_url: str = "https://graph.microsoft.com/v1.0"
    user_id: str

    def __init__(self, config: dict):
        self.headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {config["token"]}",
        }
        self.user_id = config["user_id"].strip()
        super().__init__()

    def configure(): ...

    async def set_status(
        self, status: str, emoji: str, expires: int | None = None
    ) -> str:
        logger.info("🧑‍💼 Setting Teams status...")

        response = self.post(
            path=f"/users/{self.user_id}/presence/setStatusMessage",
            json={
                "statusMessage": {
                    "message": {
                        "content": "Hey I'm currently in a meeting.",
                        "contentType": "text",
                    },
                    "expiryDateTime": {
                        "dateTime": "2022-10-18T17:05:33.2079781",
                        "timeZone": "Pacific Standard Time",
                    },
                }
            },
        )

        return response.json()


class DiscordClient: ...


class GithubClient: ...


class OutlookClientConfigurationException(Exception): ...


class MsalClient:
    # https://github.com/AzureAD/microsoft-authentication-extensions-for-python
    scopes = ["User.Read", "MailboxSettings.ReadWrite"]
    client: GraphServiceClient

    def __init__(self):
        persistence = self._build_persistence(Path(CONFIG_DIR, "token_cache.bin"))
        cache = PersistedTokenCache(persistence)

        app = PublicClientApplication(
            CLIENT_ID,
            authority="https://login.microsoftonline.com/consumers",
            token_cache=cache,
        )

        accounts = app.get_accounts()
        credentials = None
        if accounts:
            credentials = app.acquire_token_silent(self.scopes, account=accounts[0])

        if not credentials:
            print("Initiating flow to get new token...")
            # no token exists, initiate flow for new one
            flow = app.initiate_device_flow(scopes=self.scopes)
            logger.info(flow["message"])
            credentials = app.acquire_token_by_device_flow(flow=flow)

        if "access_token" in credentials:
            logger.info("✅ Credentials acquired!")
        else:
            logger.error(credentials.get("error"))
            logger.error(credentials.get("error_description"))
            logger.error(credentials.get("correlation_id"))
            raise ValueError("❌ Unable to get an access token.")

        self.client = GraphServiceClient(
            credentials=credentials,
            scopes=self.scopes,
        )

    @staticmethod
    def _build_persistence(location, fallback_to_plaintext=False):
        """Build a suitable persistence instance based your current OS"""
        try:
            return build_encrypted_persistence(location)
        except:
            if not fallback_to_plaintext:
                raise
            logger.warning("Encryption unavailable. Opting in to plain text.")
            return FilePersistence(location)

    async def set_status(self):
        # To initialize your graph_client, see https://learn.microsoft.com/en-us/graph/sdks/create-client?from=snippets&tabs=python
        request_body = MailboxSettings(
            automatic_replies_setting=AutomaticRepliesSetting(
                internal_reply_message="Hello",
                external_reply_message="Hiya",
                status=AutomaticRepliesStatus.Scheduled,
                scheduled_start_date_time=DateTimeTimeZone(
                    date_time="2025-06-28T18:00:00.0000000",
                    time_zone="UTC",
                ),
                scheduled_end_date_time=DateTimeTimeZone(
                    date_time="2025-07-02T18:00:00.0000000",
                    time_zone="UTC",
                ),
            ),
        )

        result = await self.client.me.mailbox_settings.patch(request_body)

        print(result)


def slack_test():
    import asyncio

    client = SlackClient(config={"token": "new_token"})
    response = asyncio.run(client.set_status(status="", emoji="🤖"))
    print(response)


def msal_test():
    client = MsalClient()


def discord():
    pass


if __name__ == "__main__":
    msal_test()
