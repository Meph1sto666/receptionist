import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *
from lib.types.errors import *

def errorListEmb(errorData:dict[str, dict[str, dict[str, str] | list[str]]]) -> discord.Embed:
    return discord.Embed(
        title="Available error codes",
        description="List of error codes you can input into the 'code' parameter of the command.",
        fields=[
            discord.EmbedField(
                name="Error code {e}".format(e=e),
                value=str(errorData[e]["response"]["head"])
            ) for e in errorData
        ]
    )

class ErrorCodeCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="error", description="helps you resolve your error message from the launcher") # type: ignore
    @commands.has_role(getRole("tester"))
    async def errorCode(self, ctx:discord.Message, code:str|None=None) -> None:
        # user: User = getUser(ctx.author)
        errorData = json.load(open("./data/errorcodes.json"))
        if code:
            codeData = errorData[str(code)]
            emb = discord.Embed(
                title=f"{codeData['response']['head']} {'Error {e}'.format(e=code)}",
                description=codeData["response"]["desc"],
                fields=[
                    discord.EmbedField(
                        name="Option {n}".format(n=n+1),
                        value=codeData["options"][n]
                    ) for n in range(len(codeData["options"]))
                ]
            )
            await ctx.respond(embed=emb) # type: ignore
        else:
            await ctx.respond(embed=errorListEmb(errorData)) # type: ignore
        
    @errorCode.error # type: ignore
    async def errorCodeErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        if error.__cause__.__class__ == KeyError:
            errorData = json.load(open("./data/errorcodes.json"))
            await ctx.respond(f"Error {error.__cause__.args[0]} does not exist.", embed=errorListEmb(errorData)) # type: ignore
        else:
            await ctx.respond("COPE YOU STUPID BI***. Solve it yourself!") # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(ErrorCodeCog(bot))