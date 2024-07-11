import discord
from discord.ext import commands
from lib.lang import Lang
from lib.roles import getRoles
from lib.types.errors import UserDoesNotExist
from models import User
import json
import logging
logger: logging.Logger = logging.getLogger('bot')

class FaqCog(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot

    @discord.slash_command(name="faq", description="list of frequently asked questions")  # type: ignore
    @commands.has_any_role(*getRoles(["tester"]))
    async def faq(self, ctx: discord.Message) -> None:
        faqData: list[dict[str, str]] = json.load(open("./data/files/qna.json", encoding="utf-8"))
        user: User = User.get_or_create(id=ctx.author.id)[0]
        language = Lang()
        language.loadLanguage(user.language)
        await ctx.respond(
            embed=discord.Embed(  # type: ignore
                color=discord.Colour.random(),
                title=language.translate("faq_title"),
                description=language.translate("faq_description"),
                fields=[
                    discord.EmbedField(
                        name=language.translate(k.get("q", "qna_q")),
                        value=language.translate(k.get("a", "qna_a"))
                    ) for k in faqData
                ]
            ),
            ephemeral=True
        )

    @faq.error  # type: ignore
    async def faqErr(self, ctx: discord.Message, error: discord.ApplicationCommandError) -> None:
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond(lang.translate("missing_command_permission"), ephemeral=True)  # type: ignore
        elif error.__cause__.__class__ == UserDoesNotExist:
            await ctx.respond(lang.translate("user_does_not_exist"), ephemeral=True)  # type: ignore
        else:
            logger.error(error, stack_info=True)
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True)  # type: ignore


def setup(bot: discord.Bot) -> None:
    bot.add_cog(FaqCog(bot))
