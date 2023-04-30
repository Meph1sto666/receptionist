import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *
from lib.misc import *

class ListInvites(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__()
		self.bot:discord.Bot = bot

	@discord.slash_command(name="list_invites", description="lists an users invites") # type: ignore
	@commands.has_role(getRole("tester"))
	async def listUserInvites(self, ctx:discord.Message, user_id:str|None=None) -> None:
		user:User = loadUser(int(user_id)) if user_id != None else getUser(ctx.author)
		await ctx.respond(embed=createInviteEmbed(user), ephemeral=True) # type: ignore

def setup(bot:discord.Bot) -> None:
    bot.add_cog(ListInvites(bot))