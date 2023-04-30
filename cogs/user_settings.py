import discord
from discord.ext import commands

class UserSettingsView(discord.ui.View):
	def __init__(self, *items: discord.ui.Item, timeout: float | None = 180, disable_on_timeout: bool = False) -> None: # type: ignore
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) # type: ignore
 

class UserSettings(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot

def setup(bot:discord.Bot) -> None:
    bot.add_cog(UserSettings(bot))