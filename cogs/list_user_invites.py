import discord
from discord.ext import commands
from peewee import DoesNotExist

from lib.lang import Lang
from lib.roles import getRoles
from models import User, Invite
from lib.types.errors import UserDoesNotExist


class ListInvites(commands.Cog):
	def __init__(self, bot: discord.Bot) -> None:
		super().__init__()
		self.bot: discord.Bot = bot

	@discord.slash_command(name="list_invites", description="lists a users invites")  # type: ignore
	@commands.has_any_role(*getRoles(["tester"]))
	async def listUserInvites(self, ctx: discord.Message, user_id: str | None = None) -> None:
		try:
			user: User = User.get_or_create(id=int(user_id or ctx.author.id))[0]
			invites:list[Invite] = list(Invite.select().where(Invite.user_id == user.id))
			language:Lang = Lang()
			language.loadLanguage(user.language)
			embs: list[discord.Embed] = [i.create_embed(language) for i in invites]
			await ctx.respond("" if len(embs) > 0 else language.translate("no_invites_yet"), embeds=embs, ephemeral=True)  # type: ignore
		except DoesNotExist:
			await ctx.respond(Lang().translate("no_invites_yet"), embeds=None, ephemeral=True)

	@listUserInvites.error  # type: ignore
	async def cInvErr(self, ctx: discord.Message, error: discord.ApplicationCommandError) -> None:
		if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			await ctx.respond(lang.translate("missing_command_permission"), ephemeral=True)  # type: ignore
		elif error.__cause__.__class__ == UserDoesNotExist:
			await ctx.respond(lang.translate("user_does_not_exist"))  # type: ignore
		else:
			await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True)  # type: ignore


def setup(bot: discord.Bot) -> None:
	bot.add_cog(ListInvites(bot))
