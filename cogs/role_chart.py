from hashlib import md5
import os
import discord
from discord.ext import commands
from lib.roles import getRoles
from lib.types.errors import UserDoesNotExist
import matplotlib.pyplot as plt

class RoleChartCog(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__()
		self.bot:discord.Bot = bot

	@discord.slash_command(name="role_chart", description="Pie chart showing the role distribution") # type: ignore
	@commands.has_any_role(*getRoles(["tester"]))
	async def listUserInvites(self, ctx:discord.Message) -> None:
		roles:list[discord.Role]|None = None if ctx.guild == None else list(filter(lambda x: x.name != "@everyone", ctx.guild.roles))
		_, ax = plt.subplots(figsize=(10, 6)) # type: ignore
		await ctx.guild.chunk() # type: ignore

		if roles == None: raise Exception
		data: list[int] = [len(r.members) for r in roles]
		labels: list[str] = [f"[{roles[r].name}] {data[r]}" for r in range(len(roles))] # type: ignore
		colors: list[str] = ['#{0:02x}{1:02x}{2:02x}'.format(*r.color.to_rgb()) for r in roles]

		ax.pie([d/ctx.guild.member_count for d in data], colors=colors, autopct='%1.1f%%') # type: ignore
		ax.set_title(f'Server Roles [{ctx.guild.member_count} users total]') # type: ignore
		ax.legend(labels, loc="center right", bbox_to_anchor=(0, 0)) # type: ignore

		fname:str = md5(b"".join([str(r.id).encode() for r in roles])).hexdigest()
		plt.savefig(f"./data/temp/{fname}") # type: ignore

		file = discord.File(
			f"./data/temp/{fname}.png",
       		filename=fname + ".png"
		)
		await ctx.respond(file=file) # type: ignore
		os.remove(f"./data/temp/{fname}.png")

	@listUserInvites.error # type: ignore
	async def cInvErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			await ctx.respond("You don't have the permissions to use this command.", ephemeral=True) # type: ignore
		elif error.__cause__.__class__ == UserDoesNotExist:
			await ctx.respond("User does not exist") # type: ignore
		else:
			await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore

def setup(bot:discord.Bot) -> None:
	bot.add_cog(RoleChartCog(bot))