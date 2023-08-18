from hashlib import md5
import os
import discord
from discord.ext import commands
from matplotlib.patches import Wedge
from matplotlib.text import Text
from lib.roles import getRoles
from lib.types.errors import UserDoesNotExist
import matplotlib.pyplot as plt

class RoleChartCog(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__()
		self.bot:discord.Bot = bot

	@discord.slash_command(name="role_chart", description="Pie chart showing the role distribution") # type: ignore
	@commands.has_any_role(*getRoles(["tester"]))
	async def roleChart(self, ctx:discord.Message) -> None:
		await ctx.guild.chunk() # type: ignore
		roles:list[discord.Role]|None = None if ctx.guild == None else sorted(list(filter(lambda x: x.name != "@everyone" or len(x.members)<1, ctx.guild.roles)), key=lambda s: len(s.members), reverse=True)
		_, ax = plt.subplots(figsize=(10, 6)) # type: ignore

		if roles == None or ctx.guild == None: raise Exception
		pieData: list[tuple[list[Wedge], list[Text], list[Text]]] = [
			ax.pie( # type: ignore
				[len(roles[r].members), ctx.guild.member_count-len(roles[r].members)],
				labels=["", ""],
				radius=(((len(roles))-r)/(len(roles)))*1.25, # 1.25 scale
				colors=["#{:02x}{:02x}{:02x}".format(*roles[r].color.to_rgb()), "#ffffff"],
				startangle=(360/(len(roles)))*(r-1),
				labeldistance=((len(roles))-r)/(len(roles))
			) for r in range(len(roles))
		]

		ax.legend( # type: ignore
			labels=[f"{r.name} / {len(r.members)} / "+"%1.0f%%"%(len(r.members)/ctx.guild.member_count*100) for r in roles],
            handles=[l[0][0] for l in pieData],
            bbox_to_anchor=(-.125, 0.6)
        )
		ax.set_title(f'Server Roles [{ctx.guild.member_count} users total]', fontdict={"fontsize": 18}, y=1.08) # type: ignore // -.125
		
		fname:str = md5(b"".join([str(r.id).encode() for r in roles])).hexdigest()
		plt.savefig(f"./data/temp/{fname}") # type: ignore

		file = discord.File(
			f"./data/temp/{fname}.png",
       		filename=fname + ".png"
		)
		await ctx.respond(file=file) # type: ignore
		os.remove(f"./data/temp/{fname}.png")

	@roleChart.error # type: ignore
	async def cInvErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			await ctx.respond("You don't have the permissions to use this command.", ephemeral=True) # type: ignore
		elif error.__cause__.__class__ == UserDoesNotExist:
			await ctx.respond("User does not exist") # type: ignore
		else:
			await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore

def setup(bot:discord.Bot) -> None:
	bot.add_cog(RoleChartCog(bot))