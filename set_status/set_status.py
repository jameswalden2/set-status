import emoji as emj


class SetStatus:
    def __init__(self) -> None:
        pass

    @staticmethod
    def format_emoji(emoji: str) -> str:
        emoji = emoji.strip()
        ## if emoji is a single character, convert it to a full emoji
        if len(emoji) == 1:
            return emj.demojize(emoji)

        ## if emoji is already a full emoji, return it
        if emoji.startswith(":"):
            return emoji if emoji.endswith(":") else f"{emoji}:"

        ## if emoji is text only then return with colons
        return f":{emoji}:"

    @staticmethod
    def format_status(status: str) -> str:
        return status.strip()

    def set_status(self, status: str, emoji: str, expiration: int):
        status = self.format_status(status=status)
        emoji = self.format_emoji(emoji=emoji)
