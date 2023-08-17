import os
import discord
from dotenv import load_dotenv  # type: ignore
from lib.logsetup import init_log

init_log()
load_dotenv()
intents: discord.Intents = discord.Intents.all()
intents.members = True;

bot = discord.Bot(activity=discord.activity.Game(name="/guide",url=""), intents=intents) # GITS on FA-EMU

def addExts(path:str) -> None:
    if "__pycache__" in path: return
    if os.path.isdir(path):
        for p in os.listdir(path):
            addExts(f"{path}/{p}")
    elif path.endswith(".py"):
        bot.load_extension(path[2:-3].replace("/", "."))

addExts("./cogs")

@bot.event
async def on_ready() -> None:
    # not used so far
    pass

bot.run(token=os.getenv("TOKEN"), reconnect=True)