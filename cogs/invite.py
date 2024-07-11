import discord
from discord.ext import commands
from peewee import DoesNotExist
from lib.lang import Lang
from lib.roles import getRoles
from models import Invite, User
from lib.types.errors import InviteLimitExceeded, UserDoesNotExist
import json
import logging
logger: logging.Logger = logging.getLogger('bot')

class InviteCog(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot

    @discord.slash_command(name="invite", description="create an invite link")  # type: ignore
    @commands.has_any_role(*getRoles(["tester"]))
    async def cInv(self, ctx: discord.Message) -> None:
        # print(self.bot.is_ws_ratelimited())
        inviteSettings = json.load(open("./data/invitesettings.json", "r", encoding="utf-8"))
        inv: discord.Invite = await ctx.channel.create_invite(max_age=inviteSettings["period"] * (60 ** 2 * 24),
                                                              max_uses=inviteSettings["max_uses"],
                                                              unique=True)  # type: ignore
        # user: User
        # try:
        user: User = User.get_or_create(id=ctx.author.id)[0]
        # except DoesNotExist:
        #     # Create new user.
        #     user = User(id=ctx.author.id, timezone=0, invite_permission=True, allow_ping=False,
        #                 language="en_us")
        #     user.save(force_insert=True)

        if user.is_limit_exceeded():
            raise InviteLimitExceeded("limit exceeded")

        invite = Invite(
            id=inv.id,
            created_at=inv.created_at,
            expires_at=inv.expires_at,  # type: ignore
            max_uses=inv.max_uses,  # type: ignore
            url=inv.url,  # type: ignore
            user_id=user.id
        )
        invite.save(force_insert=True)
        await ctx.respond(inv.url, ephemeral=True)  # type: ignore

    @cInv.error  # type: ignore
    async def cInvErr(self, ctx: discord.Message, error: discord.ApplicationCommandError|InviteLimitExceeded) -> None:
        lang:Lang = Lang(User.get_or_create(id=ctx.author.id)[0].language)
        if isinstance(error, discord.ApplicationCommandInvokeError): # NOTE: for some reason it's not InviteLimitExceeded but this weird invoke error
            await ctx.respond("invite_limit_exceeded.", ephemeral=True)  # type: ignore
        elif isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond(lang.translate("missing_command_permission"), ephemeral=True)  # type: ignore
        elif error.__cause__.__class__ == UserDoesNotExist:
            await ctx.respond(lang.translate("user_does_not_exist"), ephemeral=True)  # type: ignore
        else:
            logger.error(error, stack_info=True)
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True)  # type: ignore


def setup(bot: discord.Bot) -> None:
    bot.add_cog(InviteCog(bot))
