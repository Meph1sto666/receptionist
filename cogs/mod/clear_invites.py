import discord
from discord.ext import commands

from lib.lang import Lang
from lib.roles import getRoles
from models import User, Invite


class InviteClear(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot

    @discord.slash_command(name="clear_user_invites", description="prunes the users invites")  # type: ignore
    @commands.has_any_role(*getRoles(["mod", "team"]))
    async def delUserInvite(self, ctx: discord.Message, user_id: str, reason: str | None = None) -> None:
        user: User = User.get_or_create(id=int(user_id))[0]
        invites:list[Invite] = Invite.select().where(Invite.user_id == user.id)
        print(invites)
        allInvs = list(
            filter(lambda x: x.id in [i.id for i in invites], await ctx.guild.invites()))  # type: ignore

        prevLen: int = len(allInvs)

        [await i.delete(reason=reason) for i in allInvs]

        for invite in invites:
            invite.delete_by_id(invite.id)
        language = Lang()
        language.loadLanguage(user.language)
        await ctx.respond(language.translate("deleted_n_invites").format(n=prevLen))  # type: ignore

    @delUserInvite.error  # type: ignore
    async def cInvErr(self, ctx: discord.Message, error: discord.ApplicationCommandError) -> None:
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond("You don't have the permissions to use this command.", ephemeral=True)  # type: ignore
        elif error.__cause__.__class__ == FileNotFoundError:
            print(error)
            await ctx.respond("User does not exist")  # type: ignore
        else:
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True)  # type: ignore


def setup(bot: discord.Bot) -> None:
    bot.add_cog(InviteClear(bot))
