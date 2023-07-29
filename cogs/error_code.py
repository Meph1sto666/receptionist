import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *
from lib.types.errors import *

class ErrorCodeCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="error", description="helps you resolve your error message from the launcher") # type: ignore
    @commands.has_role(getRole("tester"))
    async def errorCode(self, ctx:discord.Message) -> None:
        # user: User = getUser(ctx.author)
        await ctx.respond("COPE")# type: ignore
        
    @errorCode.error # type: ignore
    async def errorCodeErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(ErrorCodeCog(bot))