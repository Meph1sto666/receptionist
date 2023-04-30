import discord
from discord.ext import commands
from discord.ui.item import Item
from lib.roles import *
from lib.types.user import *
from lib.types.errors import *
from lib.lang import *

class LangSelector(discord.ui.View):
    def __init__(self, *items: list[Item], timeout: float | None = 180, disable_on_timeout: bool = False): # type: ignore
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) # type: ignore
        sOption = discord.ui.Select( # type: ignore
            custom_id="lang",
            placeholder="Select your prefferd language",
            options=[
                discord.SelectOption(
                    label=f"{l}",
                    value=str(l)
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
    @commands.has_role(getRole("tester"))
    async def langSelect(self, ctx:discord.Message) -> None:
        await ctx.respond(view=LangSelector()) # type: ignore
        
    @langSelect.error # type: ignore
    async def langSelectErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(LanguageSelectionCog(bot))