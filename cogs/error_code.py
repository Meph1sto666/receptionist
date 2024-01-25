import typing
import discord
from discord.ext import commands
from lib.roles import getRoles
from lib.types.user import getUser, User
import json

def errorListEmb(errorData:typing.Any, user:User) -> discord.Embed:
    return discord.Embed(
        title=user.language.translate("err_cmd_available_list"),
        description=user.language.translate("err_cmd_available_list_desc"),
        fields=[
            discord.EmbedField(
                name=user.language.translate("err_cmd_errcode").format(e=e),
                value=user.language.translate(errorData[e]["response"]["head"])
            ) for e in errorData
        ]
    )

class ErrorCodeCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="error", description="helps you resolve your error message from the launcher") # type: ignore
    @commands.has_any_role(*getRoles(["tester"]))
    async def errorCode(self, ctx:discord.Message, code:str|None=None) -> None:
        user: User = getUser(ctx.author)
        errorData = json.load(open("./data/errorcodes.json", "r", encoding="utf-8"))
        if code:
            codeData = errorData[str(code)]
            emb = discord.Embed(
                title=f"{user.language.translate(codeData['response']['head'])} {user.language.translate('err_cmd_errcode').format(e=code)}",
                description=user.language.translate(codeData["response"]["desc"]),
                fields=[
                    discord.EmbedField(
                        name=user.language.translate("err_cmd_ans_option").format(n=n+1),
                        value=user.language.translate(codeData["options"][n])
                    ) for n in range(len(codeData["options"]))
                ]
            )
            await ctx.respond(embed=emb) # type: ignore
        else:
            await ctx.respond(embed=errorListEmb(errorData, user)) # type: ignore
        
    @errorCode.error # type: ignore
    async def errorCodeErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        user: User = getUser(ctx.author)
        #     await ctx.respond(f"You don't have the permissions to use this command.") # type: ignore
        if error.__cause__.__class__ == KeyError:
            errorData = json.load(open("./data/errorcodes.json", encoding="utf-8"))
            await ctx.respond(user.language.translate("err_cmd_errmsg_not_exist").format(ec=error.__cause__.args[0]), embed=errorListEmb(errorData, user)) # type: ignore // ec for error code (else translated by mtl raising error)
        else:
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(ErrorCodeCog(bot))