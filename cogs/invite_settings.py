import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *

class InviteSettingsView(discord.ui.View):
    def __init__(self, *items: discord.ui.Item, timeout: float | None = 180, disable_on_timeout: bool = False): # type: ignore
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) # type: ignore
        periodMenu = discord.ui.Select( # type: ignore
            custom_id="period",
            placeholder="Days before max invitres reset",
            options=[
                discord.SelectOption(
                    label=str(i),
                    value=str(i)
                )
                for i in [7, 14, 21, 28, 182]
            ],
            row=1
        )
        periodMenu.callback = self.cb
        self.add_item(periodMenu)# type: ignore

        maxInvMenu = discord.ui.Select( # type: ignore
            custom_id="max_invites",
            placeholder="Max invite urls",
            options=[
                discord.SelectOption(
                    label=str(i),
                    value=str(i)
                )
                for i in [1,5,10,20,25,50,75]
            ],
            row=2
        )
        maxInvMenu.callback = self.cb
        self.add_item(maxInvMenu)# type: ignore
    
    async def cb(self, interaction:discord.Interaction) -> None:
        print(interaction.data)
        setSetting(interaction.data["custom_id"], interaction.data["values"][0]) # type: ignore
        await interaction.response.defer()

class InviteSettings(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot = bot
    
    @discord.slash_command(name="invite_settings", description="modify settings for invites") # type: ignore
    @commands.has_role(getRole("tester"))
    async def cInvSettings(self, ctx:discord.Message) -> None:
        data:dict[str, int] = dict(json.load(open(sPath, "r")))
        embed = discord.Embed(
            color=discord.Color.from_rgb(255, 255, 255),
            title="Options",
            fields=[
                discord.EmbedField(
                    name=d,
                    value=str(data.get(d)),
                    inline=False
                ) for d in data
            ]
        )
        await ctx.respond(embed=embed, view=InviteSettingsView()) # type: ignore
        
    @cInvSettings.error # type: ignore
    async def cInvSettingsErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore
        
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(InviteSettings(bot))