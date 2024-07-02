from datetime import datetime as dt
import os
import discord
from discord.ext import commands
from lib.roles import getRoles
from models import User
from lib.types.errors import UserDoesNotExist
import logging
from discord.ui import Item

logger: logging.Logger = logging.getLogger('bot')

class TimezoneSettingView(discord.ui.View):
	"""
	modal for adding ping rules
	"""

	def __init__(self, user: User, *items: Item, timeout: float | None = 180,
				 disable_on_timeout: bool = False) -> None:  # type: ignore
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)  # type: ignore
		self.user: User = user
		self.timezoneSelect: discord.SelectMenu = discord.ui.Select(  # type: ignore
			custom_id='timezone_select',
			placeholder='Select your timezone. If none is selected UTC will be used!',
			min_values=1,
			max_values=1,
			options=self.getTimezoneOptions()
		)

		self.timezoneSelect.callback = self.tz_select_cb  # type: ignore
		for b in [self.timezoneSelect]:#, self.timezoneSelect  # type: ignore
			self.add_item(b)  # type: ignore

	def getTimezoneOptions(self) -> list[discord.SelectOption]:
		return [
			discord.SelectOption(
				label='UTC' + (str(i) if str(i).startswith('-') and i != 0 else f'+{i}'),
				value=str(i),
				default=i*60 == self.user.timezone
			) for i in range(-12, 13)
		]

	async def tz_select_cb(self, interaction: discord.Interaction) -> None:
		"""callback to set the users timezone"""
		self.utcOffset = int(interaction.data.get('values', [])[0])
		self.user.timezone = self.utcOffset*60
		self.user.save()
		self.timezoneSelect.options = self.getTimezoneOptions()
		await interaction.response.edit_message(view=self)

class TimezoneCog(commands.Cog):
	def __init__(self, bot: discord.Bot) -> None:
		super().__init__()
		self.bot: discord.Bot = bot

	@discord.slash_command(name="timezone", description="Set or edit your timezone")  # type: ignore
	@commands.has_any_role(*getRoles(["tester"]))
	async def setTz(self, ctx: discord.Message) -> None:
		await ctx.respond("set your Timezone", view=TimezoneSettingView(User.get_or_create(id=ctx.author.id)[0]), ephemeral=True)  # type: ignore

	@setTz.error  # type: ignore
	async def setTzErr(self, ctx: discord.Message, error: discord.ApplicationCommandError) -> None:
		raise
		if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			await ctx.respond("You don't have the permissions to use this command.", ephemeral=True)  # type: ignore
		elif error.__cause__.__class__ == UserDoesNotExist:
			await ctx.respond("User does not exist")  # type: ignore
		else:
			logger.error(error, stack_info=True)
			await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True)  # type: ignore


def setup(bot: discord.Bot) -> None:
	bot.add_cog(TimezoneCog(bot))