import discord
from discord.ext import commands
from lib.roles import getRoles
from lib.types.errors import UserDoesNotExist
import logging
logger: logging.Logger = logging.getLogger('bot')

class LauncherCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="launcher", description="get the launcher") # type: ignore
    @commands.has_any_role(*getRoles(["tester"]))
    async def getLauncher(self, ctx:discord.Message) -> None:
        await ctx.defer() # type: ignore
        await ctx.respond(
            file=discord.File( # type: ignore
			    "./data/files/fa-emu-launcher-v206.zip",
			    filename="fa-emu-launcher-v206.zip"
		    ),
            ephemeral=True
        )
        
    @getLauncher.error # type: ignore
    async def getGuideErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond(lang.translate("missing_command_permission"), ephemeral=True)  # type: ignore
        elif error.__cause__.__class__ == UserDoesNotExist:
            await ctx.respond(lang.translate("user_does_not_exist"), ephemeral=True)  # type: ignore
        else:
            logger.error(error, stack_info=True)
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(LauncherCog(bot))