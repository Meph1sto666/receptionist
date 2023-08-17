import discord
from discord.ext import commands

class HelpCog(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__()
		self.bot:discord.Bot = bot
	
	@discord.slash_command(name="help", description="Commands help") # type: ignore
	async def getGameFiles(self, ctx:discord.Message) -> None:
		pass
		# await ctx.respond("") # type: ignore
		
	@getGameFiles.error # type: ignore
	async def getGameFilesErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			await ctx.respond("You don't have the permissions to use this command.", ephemeral=True) # type: ignore
		else:
			await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore

def setup(bot:discord.Bot) -> None:
	bot.add_cog(HelpCog(bot))