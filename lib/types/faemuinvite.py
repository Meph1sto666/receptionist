from lib.lang import *
from datetime import datetime as dt
import discord

class FaEmuInvite():
    def __init__(self, id:str, created:dt, expires:dt, max_uses:int, url:str) -> None:
        self.ID:str = id
        self.CREATED_AT:dt = created
        self.EXPIRES_AT:dt = expires
        self.MAX_USES:int = max_uses
        self.URL:str = url
    
    def createEmbedField(self, language:Lang) -> discord.EmbedField:
        return discord.EmbedField(
            name=str(self.ID),
            value="\n".join([
                f"**{language.translate('created_at')}**: {self.CREATED_AT.strftime('%Y-%m-%d %H:%M')}",
                f"**{language.translate('expires_at')}**: {self.EXPIRES_AT.strftime('%Y-%m-%d %H:%M')}",
                f"**{language.translate('max_uses')}**: {self.MAX_USES}",
                f"**{language.translate('url')}**: {self.URL}"
            ])
        )