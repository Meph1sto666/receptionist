import time
from typing import Literal
import discord
from discord.ext import commands, tasks
from discord.ui.item import Item
from lib.roles import getRoles

class SetActivity(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__()
		self.bot:discord.Bot = bot
		self.index = 0
		self.quotes:list[discord.activity.BaseActivity] = [
			discord.activity.Game("with Motoko's 🐱"),
			discord.activity.Game("READ THE GUIDE"),
			discord.activity.Game("Post bugs in bug-report"),
			discord.activity.Game("crashing the server"),
			discord.activity.Game("do grenades work?"),
			discord.activity.Game("riding Tachikomas <3"),
			discord.activity.Game("with grenades")
		]
		self.modes:dict[str, tasks.Loop] = {
			'roles': self.roleMode,
			'quotes': self.quoteMode
		}
		self.mode:str|None = None
		self.roles:list[discord.Role]|None = None

	@discord.slash_command(name="set_activity", description="sets Receptionist's activity") # type: ignore
	@commands.has_any_role(*getRoles(["mod", "team"]))
	async def setActivity(self, ctx:discord.Message) -> None:
		await ctx.respond(view=ModeSelect(ctx, self), ephemeral=True)
		
	@tasks.loop(seconds=30)
	async def roleMode(self, ctx:discord.Message) -> None:
		await ctx.guild.chunk() # type: ignore
		if self.index == 0 or self.roles is None:
			self.roles = None if ctx.guild is None else sorted(list(filter(lambda x: x.name != "@everyone" or len(x.members)<1, ctx.guild.roles)), key=lambda s: len(s.members), reverse=True)
		if self.roles is None or ctx.guild is None: raise Exception
		await self.bot.change_presence(activity=discord.activity.Game(f'with {len(self.roles[self.index].members)} in {self.roles[self.index].name}'))
		self.index+=1
		if self.index >= len(self.roles):
			self.index = 0

	@tasks.loop(seconds=30)
	async def quoteMode(self, ctx:discord.Message) -> None:
		await self.bot.change_presence(activity=self.quotes[self.index])
		self.index+=1
		if self.index >= len(self.quotes):
			self.index = 0

	@setActivity.error # type: ignore
	async def cInvErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			await ctx.respond("You don't have the permissions to use this command.", ephemeral=True) # type: ignore
		elif error.__cause__.__class__ == FileNotFoundError:
			await ctx.respond("User does not exist") # type: ignore
		else:
			await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore


class ModeSelect(discord.ui.View):
	def __init__(self, ctx:discord.Message, parent:SetActivity, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False):
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
		self.parent:SetActivity = parent
		self.ctx:discord.Message = ctx
		for m in parent.modes:
			b = discord.ui.Button(
				style=discord.ButtonStyle.primary,
				label=m.upper(),
				custom_id=m
			)
			b.callback = self.setFunc
			self.add_item(b)

	async def setFunc(self, interaction:discord.Interaction) -> tasks.Loop:
		await interaction.response.defer()
		await self.ctx.delete()
		if self.parent.mode == interaction.custom_id: return
		if self.parent.mode is not None:
			self.parent.modes[self.parent.mode].cancel()
		self.parent.mode = interaction.custom_id
		self.parent.index = 0
		await self.parent.modes[interaction.custom_id].start(ctx=self.ctx)

def setup(bot:discord.Bot) -> None:
	bot.add_cog(SetActivity(bot))