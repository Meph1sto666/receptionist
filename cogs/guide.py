import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *
from lib.types.errors import *
from lib.lang import *

class GuideCmdCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="guide", description="get grims guide in your language") # type: ignore
    @commands.has_role(getRole("tester"))
    async def getGuide(self, ctx:discord.Message) -> None:
        await ctx.defer() # type: ignore
        await ctx.respond("https://docs.google.com/document/d/e/2PACX-1vTi0s72Cj-ExFSzDxO8lLtzR83zbeMuhlq_1NVQD27BM2B8OeZYellszk7rhdSQkV4jPu-b3m3giXHf/pub", file=discord.File(f'./data/files/gitsfaemusgv21_{getUser(ctx.author).language.name}.pdf')) # type: ignore
        
    @getGuide.error # type: ignore
    async def getGuideErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(GuideCmdCog(bot))