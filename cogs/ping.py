import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *
from lib.types.errors import *
from lib.misc import *

class PingCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="ping", description="check bot latency") # type: ignore
    async def cInv(self, ctx:discord.Message) -> None:
        await ctx.respond(f"Pong: *{round(self.bot.latency*1000, 3)}*ms delay.") # type: ignore
        
    @cInv.error # type: ignore
    async def cInvErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(PingCog(bot))