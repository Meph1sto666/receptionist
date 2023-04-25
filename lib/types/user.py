from datetime import datetime as dt
import os
import pickle
import discord
from lib.settings import *
import pytz

class User:
    def __init__(self, dcUser:discord.Member|discord.User) -> None:
        self.ID = dcUser.id
        self.invites:list[dict[str, dt]] = []
        self.invitePermission = True

    def cleanUpInvites(self) -> None:
        now = dt.now()
        self.invites = list(filter(lambda i: i.get("expires", now).astimezone(pytz.utc).replace(tzinfo=None) > now, self.invites))

    def isLimitExceeded(self) -> bool:
        return getSetting("max_invites") < self.getInviteAmound()

    def getInviteAmound(self) -> int:
        self.cleanUpInvites()
        return len(self.invites)

    def save(self) -> None:
        pickle.dump(self, open(getSaveFile(self.ID), "wb"))

def getSaveFile(id:int) -> str:
    return os.path.abspath(f"./data/userdata/{id}.usv")

def loadUser(id:int) -> User:
    return pickle.load(open(getSaveFile(id), "rb"))

def getUser(member:discord.Member|discord.User) -> User:
    try:
        return loadUser(member.id)
    except:
        return User(member)