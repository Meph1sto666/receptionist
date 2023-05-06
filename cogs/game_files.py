import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *
from lib.types.errors import *
from lib.lang import *

class GameFilesCmdCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="game_files", description="get a URL to the game files") # type: ignore
    @commands.has_role(getRole("tester"))
    async def getGameFiles(self, ctx:discord.Message) -> None:
        await ctx.respond("https://drive.google.com/file/d/1n47SAqOrjZdDclKytGfRM0YmU4hQkTrC/view") # type: ignore
        
    @getGameFiles.error # type: ignore
    async def getGameFilesErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore

def setup(bot:discord.Bot) -> None:
    bot.add_cog(GameFilesCmdCog(bot))