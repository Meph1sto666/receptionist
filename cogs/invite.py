import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *

class InviteLimitExceeded(PermissionError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    
    

class Invite(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot = bot
    
    @discord.slash_command(name="invite", description="create an invite line for one person") # type: ignore
    @commands.has_role(getRole("tester"))
    async def cInv(self, ctx:discord.Message) -> None:
        inv:discord.Invite = await ctx.channel.create_invite(max_age=604800, max_uses=1, unique=True) # type: ignore
        user = getUser(ctx.author)
        if user.isLimitExceeded(): raise InviteLimitExceeded("limit exceeded")
        user.invites.append({
            "created": inv.created_at, # type: ignore
            "expires": inv.expires_at # type: ignore
        }) # type: ignore
        user.save()
        await ctx.respond(inv.url) # type: ignore
        
    @cInv.error # type: ignore
    async def cInvErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore
        
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(Invite(bot))