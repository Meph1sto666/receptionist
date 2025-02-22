import os
import discord
from discord.ext import commands
from lib.lang import Lang
from lib.roles import getRoles
from lib.types.errors import UserDoesNotExist
from models import User
import logging
logger: logging.Logger = logging.getLogger('bot')

class GuideCmdCog(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot

    @discord.slash_command(name="guide", description="get Grim's guide in your language")  # type: ignore
    @commands.has_any_role(*getRoles(["tester"]))
    async def getGuide(self, ctx: discord.Message) -> None:
        await ctx.defer(ephemeral=True)  # type: ignore
        language = Lang()
        language.loadLanguage(User.get_or_create(id=ctx.author.id)[0].language)
        guidePath: str = f'./data/files/gitsfaemusgv21_{language.name}.pdf'
        await ctx.respond(
            "https://docs.google.com/document/d/e/2PACX-1vTi0s72Cj-ExFSzDxO8lLtzR83zbeMuhlq_1NVQD27BM2B8OeZYellszk7rhdSQkV4jPu-b3m3giXHf/pub",
            file=discord.File(f'./data/files/gitsfaemusgv21_en_en.pdf' if not os.path.exists(guidePath) else guidePath),
            ephemeral=True
        )  # type: ignore

    @discord.slash_command(name="rtfm", description="read the fucking manual (same as /guide)")  # type: ignore
    @commands.has_any_role(*getRoles(["tester"]))
    async def getGuide(self, ctx: discord.Message) -> None:
        await ctx.defer(ephemeral=True)  # type: ignore
        language = Lang()
        language.loadLanguage(User.get_or_create(id=ctx.author.id)[0].language)
        guidePath: str = f'./data/files/gitsfaemusgv21_{language.name}.pdf'
        await ctx.respond(
            "https://docs.google.com/document/d/e/2PACX-1vTi0s72Cj-ExFSzDxO8lLtzR83zbeMuhlq_1NVQD27BM2B8OeZYellszk7rhdSQkV4jPu-b3m3giXHf/pub",
            file=discord.File(f'./data/files/gitsfaemusgv21_en_en.pdf' if not os.path.exists(guidePath) else guidePath),
            ephemeral=True
        )  # type: ignore

    @getGuide.error  # type: ignore
    async def getGuideErr(self, ctx: discord.Message, error: discord.ApplicationCommandError) -> None:
        lang:Lang = Lang(User.get_or_create(id=ctx.author.id)[0].language)
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond(lang.translate("missing_command_permission"), ephemeral=True)  # type: ignore
        elif error.__cause__.__class__ == UserDoesNotExist:
            await ctx.respond(lang.translate("user_does_not_exist"), ephemeral=True)  # type: ignore
        else:
            logger.error(error, stack_info=True)
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True)  # type: ignore


def setup(bot: discord.Bot) -> None:
    bot.add_cog(GuideCmdCog(bot))
