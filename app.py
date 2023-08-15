import os
import discord
from dotenv import load_dotenv # type: ignore
from lib.logsetup import LOGGING_CNFG # type: ignore

load_dotenv()
bot = discord.Bot(activity=discord.activity.Game(name="Nothing",url="")) # GITS on FA-EMU

intents: discord.Intents = discord.Intents.all()
intents.members = True;

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
    pass

bot.run(token=os.getenv("TOKEN"), reconnect=True)