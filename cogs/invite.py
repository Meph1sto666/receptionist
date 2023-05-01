import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *
from lib.types.errors import *
from lib.types.faemuinvite import FaEmuInvite
from lib.misc import *

class InviteCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="invite", description="create an invite link") # type: ignore
    @commands.has_role(getRole("tester"))
    async def cInv(self, ctx:discord.Message) -> None:
        inv:discord.Invite = await ctx.channel.create_invite(max_age=604800, max_uses=1, unique=True) # type: ignore
        user: User = getUser(ctx.author)
        if user.isLimitExceeded(): raise InviteLimitExceeded("limit exceeded")
        user.invites.append(FaEmuInvite(
            inv.id, # type: ignore
            inv.created_at, # type: ignore
            inv.expires_at, # type: ignore
            inv.max_uses, # type: ignore
            inv.url # type: ignore
        ))
        user.save()
        await ctx.respond(inv.url, embed=createInviteEmbed(user)) # type: ignore
        
    @cInv.error # type: ignore
    async def cInvErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(InviteCog(bot))