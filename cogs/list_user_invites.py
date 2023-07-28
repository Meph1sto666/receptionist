import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *
# from lib.misc import *

class ListInvites(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__()
		self.bot:discord.Bot = bot

	@discord.slash_command(name="list_invites", description="lists a users invites") # type: ignore
	@commands.has_role(getRole("tester"))
	async def listUserInvites(self, ctx:discord.Message, user_id:str|None=None) -> None:
		user:User = loadUser(int(user_id)) if user_id != None else getUser(ctx.author)
		embs: list[discord.Embed] = [i.createEmbed(user.language) for i in user.invites]
		await ctx.respond("" if len(embs) > 0 else user.language.translate("no_invites_yet"), embeds=embs, ephemeral=True) # type: ignore

	@listUserInvites.error # type: ignore
	async def cInvErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		await ctx.respond(f"User does not exist") # type: ignore
def setup(bot:discord.Bot) -> None:
    bot.add_cog(ListInvites(bot))