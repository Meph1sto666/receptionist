import discord
from discord.ext import commands
from lib.roles import getRoles
from lib.settings import sPath, setSetting
from lib.lang import Lang
import json
from lib.types.user import getUser

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
        await interaction.response.edit_message(embed=createSettingsEmbed())
        
class InviteSettings(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="invite_settings", description="modify settings for invites") # type: ignore
    @commands.has_any_role(*getRoles(["mod", "team"]))
    async def cInvSettings(self, ctx:discord.Message) -> None:
        await ctx.respond(embed=createSettingsEmbed(), view=InviteSettingsView(lang=getUser(ctx.author).language), ephemeral=True) # type: ignore
        
    @cInvSettings.error # type: ignore
    async def cInvSettingsErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond("You don't have the permissions to use this command.", ephemeral=True) # type: ignore
        else:
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore
        

def createSettingsEmbed() -> discord.Embed:
    data:dict[str, int] = dict(json.load(open(sPath, "r", encoding="utf-8")))
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