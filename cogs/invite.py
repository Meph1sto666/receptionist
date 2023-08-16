import discord
from discord.ext import commands
from lib.roles import *
from lib.types.user import *
from lib.types.errors import *
from lib.types.faemuinvite import FaEmuInvite
# from lib.misc import *

class InviteCog(commands.Cog):
    def __init__(self, bot:discord.Bot) -> None:
        super().__init__()
        self.bot:discord.Bot = bot
    
    @discord.slash_command(name="invite", description="create an invite link") # type: ignore
    @commands.has_any_role(*getRoles(["tester"]))
    async def cInv(self, ctx:discord.Message) -> None:
        # print(self.bot.is_ws_ratelimited())
        inviteSettings = json.load(open("./data/invitesettings.json", "r", encoding="utf-8"))
        inv:discord.Invite = await ctx.channel.create_invite(max_age=inviteSettings["period"]*(60**2*24), max_uses=inviteSettings["max_uses"], unique=True) # type: ignore
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
        await ctx.respond(inv.url, ephemeral=True) # type: ignore
        
    @cInv.error # type: ignore
    async def cInvErr(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond(f"You don't have the permissions to use this command.", ephemeral=True) # type: ignore
        else:
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True) # type: ignore
        
def setup(bot:discord.Bot) -> None:
    bot.add_cog(InviteCog(bot))