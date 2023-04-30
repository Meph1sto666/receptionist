import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *

class InviteClear(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__()
		self.bot:discord.Bot = bot

	@discord.slash_command(name="clear_user_invites", description="redems the users invites") # type: ignore
	@commands.has_role(getRole("tester"))
	async def delUserInvite(self, ctx:discord.Message, user_id:str, reason:str|None=None) -> None:
		user: User = loadUser(int(user_id))
		allInvs = list(filter(lambda x: x.id in [i.ID for i in user.invites], await ctx.guild.invites())) # type: ignore
		prevLen:int = len(allInvs)
		[await i.delete(reason=reason) for i in allInvs]
		user.invites.clear()
		user.save()
		await ctx.respond(f"Deleted {prevLen} invites") # type: ignore

def setup(bot:discord.Bot) -> None:
    bot.add_cog(InviteClear(bot))