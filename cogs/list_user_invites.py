import discord
from discord.ext import commands
from lib.roles import getRoles
from lib.types.user import User, getUser, loadUser
from lib.types.errors import UserDoesNotExist

class ListInvites(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__()
		self.bot:discord.Bot = bot

	@discord.slash_command(name="list_invites", description="lists a users invites") # type: ignore
	@commands.has_any_role(*getRoles(["tester"]))
	async def listUserInvites(self, ctx:discord.Message, user_id:str|None=None) -> None:
		user:User = loadUser(int(user_id)) if user_id != None else getUser(ctx.author)
		embs:list[discord.Embed] = [i.createEmbed(user.language) for i in user.invites]
		await ctx.respond("" if len(embs) > 0 else user.language.translate("no_invites_yet"), embeds=embs, ephemeral=True) # type: ignore

	@listUserInvites.error # type: ignore
	async def cInvErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			await ctx.respond("You don't have the permissions to use this command.", ephemeral=True) # type: ignore
		elif error.__cause__.__class__ == UserDoesNotExist:
			await ctx.respond("User does not exist") # type: ignore
		else:
			await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore

def setup(bot:discord.Bot) -> None:
    bot.add_cog(ListInvites(bot))