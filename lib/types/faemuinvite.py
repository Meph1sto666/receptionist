import random
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
    
    def createEmbed(self, language:Lang) -> discord.Embed:
        emb = discord.Embed(
            title=str(self.URL),
            color=discord.Colour.random(),
            timestamp=dt.now(),
            fields=[
                discord.EmbedField(name=language.translate('created_at'),value=self.CREATED_AT.strftime('%Y-%m-%d %H:%M'),inline=True),
                discord.EmbedField(name=language.translate('expires_at'),value=self.EXPIRES_AT.strftime('%Y-%m-%d %H:%M'),inline=True),
                discord.EmbedField(name=language.translate('max_uses'),value=str(self.MAX_USES),inline=True)
            ],
            url=self.URL
        )
        emb.set_footer(text=f"at least they did not read page {random.randrange(1, 100)} of the guide".upper())
        return emb