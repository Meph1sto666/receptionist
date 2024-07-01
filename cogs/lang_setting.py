import discord
from discord.ext import commands
from discord.ui.item import Item
from lib.types.errors import UserDoesNotExist
from models import User
from lib.lang import getAvialLangs, Lang


class LangSelector(discord.ui.View):
    def __init__(self, user: User, *items: list[Item], timeout: float | None = 180,
                 disable_on_timeout: bool = False):  # type: ignore
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)  # type: ignore
        language = Lang()
        language.loadLanguage(user.language)
        sOption = discord.ui.Select(  # type: ignore
            custom_id="lang",
            placeholder=language.translate("select_lang"),
            options=[
                discord.SelectOption(
                    label=language.translate(l),
                    value=str(l),
                    default=language.name == l
                )
                for l in getAvialLangs()
            ]
        )
        sOption.callback = self.cb
        self.add_item(sOption)  # type: ignore

    async def cb(self, interaction: discord.Interaction) -> None:
        user: User = User.get_or_create(id=interaction.user.id)[0]
        selection: str = str(dict(interaction.data).get("values", None)[0])  # type:ignore
        user.language = selection
        user.save()
        await interaction.response.defer()
        await interaction.delete_original_response(delay=5)


class LanguageSelectionCog(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot

    @discord.slash_command(name="language", description="change your language")  # type: ignore
    async def langSelect(self, ctx: discord.Message) -> None:
        user: User = User.get_or_create(id=ctx.author.id)[0]
        await ctx.respond(view=LangSelector(user), ephemeral=True)  # type: ignore

    @langSelect.error  # type: ignore
    async def langSelectErr(self, ctx: discord.Message, error: discord.ApplicationCommandError) -> None:
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond("You don't have the permissions to use this command.", ephemeral=True)  # type: ignore
        elif error.__cause__.__class__ == UserDoesNotExist:
            await ctx.respond("User does not exist")  # type: ignore
        else:
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True)  # type: ignore


def setup(bot: discord.Bot) -> None:
    bot.add_cog(LanguageSelectionCog(bot))
