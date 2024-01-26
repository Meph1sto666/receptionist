import discord
from discord.ext import commands
from lib.roles import getRoles
from lib.types.user import User, loadUser

class InviteClear(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__()
		self.bot:discord.Bot = bot

	@discord.slash_command(name="clear_user_invites", description="prunes the users invites") # type: ignore
	@commands.has_any_role(*getRoles(["mod", "team"]))
	async def delUserInvite(self, ctx:discord.Message, user_id:str, reason:str|None=None) -> None:
		user: User = loadUser(int(user_id))
		allInvs = list(filter(lambda x: x.id in [i.ID for i in user.invites], await ctx.guild.invites())) # type: ignore
		prevLen:int = len(allInvs)
		[await i.delete(reason=reason) for i in allInvs]
		user.invites.clear()
		user.save()
		await ctx.respond(user.language.translate("deleted_n_invites").format(n=prevLen)) # type: ignore

	@delUserInvite.error # type: ignore
	async def cInvErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			await ctx.respond("You don't have the permissions to use this command.", ephemeral=True) # type: ignore
		elif error.__cause__.__class__ == FileNotFoundError:
			await ctx.respond("User does not exist") # type: ignore
		else:
			await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore

def setup(bot:discord.Bot) -> None:
	bot.add_cog(InviteClear(bot))