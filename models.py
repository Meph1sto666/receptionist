import os
import discord
import random

from peewee import *

from lib.settings import get_setting
from lib.lang import Lang
from datetime import datetime as dt

db = SqliteDatabase(os.getenv("DB_PATH"), pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(primary_key=True)
    timezone = IntegerField()
    invite_permission = BooleanField()
    allow_ping = BooleanField()
    language = TextField()

    def get_mention_str(self) -> str:
        """returns the user mention string <@discord_user_id>"""
        return f'<@{self.id}>'

    def is_limit_exceeded(self) -> bool:
        invites = Invite.select().where(Invite.user_id == self.id).count()
        return get_setting("max_invites") < invites


class Invite(BaseModel):
    id = TextField(primary_key=True)
    created_at = DateTimeField()
    expires_at = DateTimeField()
    max_uses = IntegerField()
    url = TextField()
    user_id = ForeignKeyField(User, backref='invites', null=False)

    def create_embed(self, language: Lang) -> discord.Embed:
        emb = discord.Embed(
            title=str(self.url),
            color=discord.Colour.random(),
            timestamp=dt.now(),
            fields=[
                discord.EmbedField(name=language.translate('created_at'),
                                   value=f"{self.created_at.year}-{self.created_at.month}-{self.created_at.day}"
                                         f" {self.created_at.hour}:{self.created_at.minute}", inline=True),
                discord.EmbedField(name=language.translate('expires_at'),
                                   value=f"{self.expires_at.year}-{self.expires_at.month}-{self.expires_at.day}"
                                         f" {self.expires_at.hour}:{self.expires_at.minute}", inline=True),
                discord.EmbedField(name=language.translate('max_uses'), value=str(self.max_uses), inline=True)
            ],
            url=self.URL
        )
        emb.set_footer(text=f"at least they did not read page {random.randrange(1, 100)} of the guide".upper())
        return emb


class PingRule(BaseModel):
    id = AutoField(primary_key=True)
    start = DateTimeField()
    end = DateTimeField()
    creation_time = TextField()
    user_id = ForeignKeyField(User, backref="ping_rules", null=False)
