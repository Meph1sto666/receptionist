import discord
from discord.ext import commands
from lib.roles import getRoles

class GameFilesCmdCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="game_files", description="get a URL to the game files") # type: ignore
    @commands.has_any_role(*getRoles(["tester"]))
    async def getGameFiles(self, ctx:discord.Message) -> None:
        await ctx.respond("https://drive.google.com/file/d/1n47SAqOrjZdDclKytGfRM0YmU4hQkTrC/view") # type: ignore
        
    @getGameFiles.error # type: ignore
    async def getGameFilesErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond(lang.translate("missing_command_permission"), ephemeral=True)  # type: ignore
        else:
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore

def setup(bot:discord.Bot) -> None:
    bot.add_cog(GameFilesCmdCog(bot))