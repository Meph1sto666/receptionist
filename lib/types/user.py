from datetime import datetime as dt
import os
import dill
import discord
from lib.lang import *
from lib.settings import *
from lib.types.faemuinvite import FaEmuInvite
import pytz

class User:
    def __init__(self, dcUser:discord.Member|discord.User) -> None:
        self.ID: int = dcUser.id
        self.invites:list[FaEmuInvite] = []
        self.invitePermission = True
        # self.language:Lang = Lang()

    def cleanUpInvites(self) -> None:
        now:dt = dt.now()
        self.invites = list(filter(lambda i: i.EXPIRES_AT.astimezone(pytz.utc).replace(tzinfo=None) > now, self.invites)) # type: ignore

    def isLimitExceeded(self) -> bool:
        return getSetting("max_invites") < self.getInviteAmound()

    def getInviteAmound(self) -> int:
        self.cleanUpInvites()
        return len(self.invites)

    def save(self) -> None:
        dill.dump(self, open(getSaveFile(self.ID), "wb")) # type: ignore

def getSaveFile(id:int) -> str:
    return os.path.abspath(f"./data/userdata/{id}.usv")

def loadUser(id:int) -> User:
    return dill.load(open(getSaveFile(id), "rb")) # type: ignore

def getUser(member:discord.Member|discord.User) -> User:
    try:
        return loadUser(member.id)
    except:
        return User(member)