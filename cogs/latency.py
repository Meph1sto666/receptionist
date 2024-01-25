import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *
from lib.types.errors import *
from lib.misc import *

class LatencyCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="latency", description="check bot latency") # type: ignore
    async def cInv(self, ctx:discord.Message) -> None:
        await ctx.respond(f"Pong: *{round(self.bot.latency*1000, 3)}*ms delay. [Rate limited: {self.bot.is_ws_ratelimited()}]") # type: ignore
        
    @cInv.error # type: ignore
    async def cInvErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond("You don't have the permissions to use this command.", ephemeral=True) # type: ignore
        elif error.__cause__.__class__ == UserDoesNotExist:
            await ctx.respond("User does not exist") # type: ignore
        else:
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(LatencyCog(bot))