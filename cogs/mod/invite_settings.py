import discord
from discord.ext import commands
from lib.roles import getRoles
from lib.settings import sPath, set_setting
from lib.lang import Lang
import json
from models import User
from lib.types.errors import UserDoesNotExist
import logging
logger: logging.Logger = logging.getLogger('bot')

class InviteSettingsView(discord.ui.View):
    # TODO: handle lang text to Lang obj conversion
    def __init__(self, *items: discord.ui.Item, timeout: float | None = 180, disable_on_timeout: bool = False, lang: Lang) -> None:  # type: ignore
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)  # type: ignore
        self.lang = lang
        options: list[discord.ui.Select[discord.SelectOption]] = [  # type: ignore
            discord.ui.Select(  # type: ignore
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
            discord.ui.Select(  # type: ignore
                custom_id="max_invites",
                placeholder=lang.translate("max_invites_setting"),
                options=[
                    discord.SelectOption(
                        label=str(i),
                        value=str(i)
                    )
                    for i in [1, 2, 5, 10, 15, 20]
                ]
            ),
            discord.ui.Select(  # type: ignore
                custom_id="max_uses",
                placeholder=lang.translate("max_uses_setting"),
                options=[
                    discord.SelectOption(
                        label=str(i),
                        value=str(i)
                    )
                    for i in [1, 2, 5, 10, 15, 20, 0]
                ]
            )
        ]
        for o in options:
            o.callback = self.cb
            self.add_item(o)  # type: ignore

    async def cb(self, interaction: discord.Interaction) -> None:
        # print(interaction.data)
        set_setting(interaction.data["custom_id"], int(interaction.data["values"][0]))  # type: ignore
        await interaction.response.edit_message(embed=createSettingsEmbed(self.lang))


class InviteSettings(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot

    @discord.slash_command(name="invite_settings", description="modify settings for invites")  # type: ignore
    @commands.has_any_role(*getRoles(["mod", "team"]))
    async def cInvSettings(self, ctx: discord.Message) -> None:
        lang:Lang = Lang(User.get_or_create(id=ctx.author.id)[0].language)
        await ctx.respond(embed=createSettingsEmbed(lang), view=InviteSettingsView(lang=lang),
                          ephemeral=True)  # type: ignore

    @cInvSettings.error  # type: ignore
    async def cInvSettingsErr(self, ctx: discord.Message, error: discord.ApplicationCommandError) -> None:
        lang:Lang = Lang(User.get_or_create(id=ctx.author.id)[0].language)
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond(lang.translate("missing_command_permission"), ephemeral=True)  # type: ignore
        elif error.__cause__.__class__ == UserDoesNotExist:
            await ctx.respond(lang.translate("user_does_not_exist"))  # type: ignore
        else:
            logger.error(error, stack_info=True)
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True)  # type: ignore


def createSettingsEmbed(lang:Lang) -> discord.Embed:
    data: dict[str, int] = dict(json.load(open(sPath, "r", encoding="utf-8")))
    embed = discord.Embed(
        color=discord.Color.from_rgb(255, 255, 255),
        title=lang.translate("options"),
        fields=[
            discord.EmbedField(
                name=d,
                value=str(data.get(d)),
                inline=False
            ) for d in data
        ]
    )
    return embed


def setup(bot: discord.Bot) -> None:
    bot.add_cog(InviteSettings(bot))
