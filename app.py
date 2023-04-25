import os
import discord
from dotenv import load_dotenv # type: ignore
from lib.logsetup import LOGGING_CNFG # type: ignore

load_dotenv()
bot = discord.Bot()

intents = discord.Intents.all()
intents.members = True;

def addExts(path:str) -> None:
    if "__pycache__" in path: return
    if os.path.isdir(path):
        for p in os.listdir(path):
            addExts(f"{path}/{p}")
    else:
        bot.load_extension(path[2:-3].replace("/", "."))

addExts("./cogs")
bot.run(token=os.getenv("TOKEN"), reconnect=True)