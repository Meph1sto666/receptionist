from datetime import datetime as dt
from datetime import time
import os
import pickle # type: ignore
import discord
from lib.lang import *
from lib.types.errors import *
from lib.settings import *
from lib.types.faemuinvite import FaEmuInvite
import pytz
import logging
logger:logging.Logger = logging.getLogger('bot')
VERSION:str = '20240127'

class User:
    def __init__(self, dcUser:discord.Member|discord.User) -> None:
        logger.info(f'creating new user {dcUser.id}')
        self.version:str = VERSION
        self.ID: int = dcUser.id
        self.invites:list[FaEmuInvite] = []
        self.invitePermission = True
        self.language:Lang = Lang()

        self.allowPing = False
        self.allowedPingTimes:list[tuple[time, time, bool, str]] = []

    def getMentionStr(self) -> str:
        "returns the user mention string <@discord_user_id>"
        return f'<@{self.ID}>'

    def cleanUpInvites(self) -> None:
        now:dt = dt.now()
        self.invites = list(filter(lambda i: i.EXPIRES_AT.astimezone(pytz.utc).replace(tzinfo=None) > now, self.invites)) # type: ignore

    def isLimitExceeded(self) -> bool:
        return getSetting("max_invites") < self.getInviteAmount()

    def getInviteAmount(self) -> int:
        self.cleanUpInvites()
        return len(self.invites)

    def save(self) -> None:
        pickle.dump(self, open(getSaveFile(self.ID), "wb")) # type: ignore

    def migrate(self) -> None:
        "adds possibly missing attributes"
        if not getattr(self, 'ping', False):
            self.allowPing = False
        if not getattr(self, 'allowedPingTimes', False):
            self.allowedPingTimes = []
        self.version = VERSION

def getSaveFile(id:int) -> str:
    return os.path.abspath(f"./data/userdata/{id}.usv")

def loadUser(id:int) -> User:
    "loads the user object from ./data/userdata/ and updates attributes if versions don't match"
    u:User = pickle.load(open(getSaveFile(id), "rb")) # type: ignore
    if not u.version == VERSION:
        logger.warn(f'User version out of date, migrating {u.version} to {VERSION}')
        u.migrate()
    return u

def getUser(member:discord.Member|discord.User|None) -> User:
    if member == None: raise UserDoesNotExist(member)
    try:
        return loadUser(member.id)
    except Exception as e:
        logger.error(e)
        u:User = User(member)
        return u

def delUser(id:int) -> None:
    "deletes a user file from ./data/userdata/ by its id"
    logger.info(f'deleting user {id}')
    if os.path.exists(getSaveFile(id)):
        os.remove(getSaveFile(id))