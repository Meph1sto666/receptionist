import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *

class InviteSettingsView(discord.ui.View):
    def __init__(self, *items: discord.ui.Item, timeout: float | None = 180, disable_on_timeout: bool = False, lang:Lang) -> None: # type: ignore
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) # type: ignore
        options:list[discord.ui.Select[discord.SelectOption]] = [ # type: ignore
            discord.ui.Select( # type: ignore
                custom_id="period",
                placeholder=lang.translate("max_inv_reset_delay_setting"),
                options=[
                    discord.SelectOption(
                        label=f"{i} days",
                        value=str(i)
                    )
                    for i in [7, 14, 21, 28, 182, 365]
                ]
            ),
            discord.ui.Select( # type: ignore
                custom_id="max_invites",
                placeholder=lang.translate("max_invites_setting"),
                options=[
                    discord.SelectOption(
                        label=str(i),
                        value=str(i)
                    )
                    for i in [1,2,5,10,15,20]
                ]
            ),
            discord.ui.Select( # type: ignore
                custom_id="max_uses",
                placeholder=lang.translate("max_uses_setting"),
                options=[
                    discord.SelectOption(
                        label=str(i),
                        value=str(i)
                    )
                    for i in [1,2,5,10,15,20,0]
                ]
            )
        ]
        for o in options:
            o.callback = self.cb
            self.add_item(o)# type: ignore
    
    async def cb(self, interaction:discord.Interaction) -> None:
        # print(interaction.data)
        setSetting(interaction.data["custom_id"], int(interaction.data["values"][0])) # type: ignore
        await interaction.response.edit_message(embed=createSetingsEmbed())
        
class InviteSettings(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="invite_settings", description="modify settings for invites") # type: ignore
    @commands.has_role(getRole("tester"))
    async def cInvSettings(self, ctx:discord.Message) -> None:
        await ctx.respond(embed=createSetingsEmbed(), view=InviteSettingsView(lang=getUser(ctx.author).language), ephemeral=True) # type: ignore
        
    @cInvSettings.error # type: ignore
    async def cInvSettingsErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```", ephemeral=True) # type: ignore
        

def createSetingsEmbed() -> discord.Embed:
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
    return embed

def setup(bot:discord.Bot) -> None:
    bot.add_cog(InviteSettings(bot))