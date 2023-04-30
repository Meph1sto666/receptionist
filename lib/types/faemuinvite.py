from datetime import datetime as dt
import discord

class FaEmuInvite():
    def __init__(self, id:str, created:dt, expires:dt, max_uses:int, url:str) -> None:
        self.ID:str = id
        self.CREATED_AT:dt = created
        self.EXPIRES_AT:dt = expires
        self.MAX_USES:int = max_uses
        self.URL:str = url
    
    def createEmbedField(self) -> discord.EmbedField:
        return discord.EmbedField(
            name=str(self.ID),
            value="\n".join([
                f"**Created at**: {self.CREATED_AT.strftime('%Y-%m-%d %H:%M')}",
                f"**Expires at**: {self.EXPIRES_AT.strftime('%Y-%m-%d %H:%M')}",
                f"**Max uses**: {self.MAX_USES}",
                f"**URL**: {self.URL}"
            ])
        )