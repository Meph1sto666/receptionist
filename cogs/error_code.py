import typing
import discord
from discord.ext import commands

from lib.lang import Lang
from lib.roles import getRoles
from models import User
import json


def errorListEmb(errorData: typing.Any, user: User) -> discord.Embed:
    language = Lang()
    language.loadLanguage(user.language)
    return discord.Embed(
        title=language.translate("err_cmd_available_list"),
        description=language.translate("err_cmd_available_list_desc"),
        fields=[
            discord.EmbedField(
                name=language.translate("err_cmd_errcode").format(e=e),
                value=language.translate(errorData[e]["response"]["head"])
            ) for e in errorData
        ]
    )


class ErrorCodeCog(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot

    @discord.slash_command(name="error",
                           description="helps you resolve error messages thrown by the launcher")  # type: ignore
    @commands.has_any_role(*getRoles(["tester"]))
    async def errorCode(self, ctx: discord.Message, code: str | None = None) -> None:
        user: User = User.get_or_create(id=ctx.author.id)[0]
        errorData = json.load(open("./data/errorcodes.json", "r", encoding="utf-8"))
        if code:
            codeData = errorData[str(code)]
            language = Lang()
            language.loadLanguage(user.language)
            emb = discord.Embed(
                title=f"{language.translate(codeData['response']['head'])} {language.translate('err_cmd_errcode').format(e=code)}",
                description=language.translate(codeData["response"]["desc"]),
                fields=[
                    discord.EmbedField(
                        name=language.translate("err_cmd_ans_option").format(n=n + 1),
                        value=language.translate(codeData["options"][n])
                    ) for n in range(len(codeData["options"]))
                ]
            )
            await ctx.respond(embed=emb)  # type: ignore
        else:
            await ctx.respond(embed=errorListEmb(errorData, user))  # type: ignore

    @errorCode.error  # type: ignore
    async def errorCodeErr(self, ctx: discord.Message, error: discord.ApplicationCommandError) -> None:
        user: User = User.get_or_create(id=ctx.author.id)[0]
        #     await ctx.respond(f"You don't have the permissions to use this command.") # type: ignore
        if error.__cause__.__class__ == KeyError:
            errorData = json.load(open("./data/errorcodes.json", encoding="utf-8"))
            language = Lang()
            language.loadLanguage(user.language)
            await ctx.respond(language.translate("err_cmd_errmsg_not_exist").format(ec=error.__cause__.args[0]),
                              embed=errorListEmb(errorData,
                                                 user))  # type: ignore // ec for error code (else translated by mtl raising error)
        else:
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True)  # type: ignore


def setup(bot: discord.Bot) -> None:
    bot.add_cog(ErrorCodeCog(bot))
