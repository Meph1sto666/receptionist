import discord
from discord.ext import commands
from discord.ui.item import Item
from lib.types.user import User, getUser
from lib.lang import getAvialLangs

class LangSelector(discord.ui.View):
    def __init__(self, user:User, *items: list[Item], timeout: float | None = 180, disable_on_timeout: bool = False): # type: ignore
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) # type: ignore
        sOption = discord.ui.Select( # type: ignore
            custom_id="lang",
            placeholder=user.language.translate("select_lang"),
            options=[
                discord.SelectOption(
                    label=user.language.translate(l),
                    value=str(l),
                    default=user.language.name==l
                )
                for l in getAvialLangs()
            ]
        )
        sOption.callback = self.cb
        self.add_item(sOption) # type: ignore

    async def cb(self, interaction:discord.Interaction) -> None:
        user: User = getUser(interaction.user)
        selection:str = str(dict(interaction.data).get("values", None)[0]) # type:ignore
        user.language.loadLanguage(selection)
        user.save()
        await interaction.response.defer()
        await interaction.delete_original_response(delay=5)

class LanguageSelectionCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="language", description="change your language") # type: ignore
    async def langSelect(self, ctx:discord.Message) -> None:
        user: User = getUser(ctx.author)
        await ctx.respond(view=LangSelector(user), ephemeral=True) # type: ignore
        
    @langSelect.error # type: ignore
    async def langSelectErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond("You don't have the permissions to use this command.", ephemeral=True) # type: ignore
        else:
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(LanguageSelectionCog(bot))