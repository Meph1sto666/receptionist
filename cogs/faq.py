import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *
from lib.types.errors import *

class FaqCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="faq", description="list of frequently asked questions") # type: ignore
    @commands.has_role(getRole("tester"))
    async def faq(self, ctx:discord.Message) -> None:
        faqData:list[dict[str, str]] = json.load(open("./data/files/qna.json"))
        user: User = getUser(ctx.author)
        await ctx.respond(embed=discord.Embed( # type: ignore
            color=discord.Colour.random(),
            title=user.language.translate("faq_title"),
            description=user.language.translate("faq_description"),
            fields=[
                discord.EmbedField(
                    name=user.language.translate(k.get("q", "qna_q")),
                    value=user.language.translate(k.get("a", "qna_a"))
                ) for k in faqData
            ]
        ))            

    @faq.error # type: ignore
    async def faqErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(FaqCog(bot))