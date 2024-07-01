from datetime import datetime as dt
import os
import discord
from discord.ext import commands
from lib.roles import getRoles
from models import User
from lib.types.errors import UserDoesNotExist
import logging

logger: logging.Logger = logging.getLogger('bot')


class PingCog(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot

    @discord.slash_command(name="ping", description="pings for a lobby")  # type: ignore
    # @commands.cooldown(1, 3600, type=commands.cooldowns.BucketType.guild)
    @commands.has_any_role(*getRoles(["tester"]))
    async def lobbyPing(self, ctx: discord.Message, message: str) -> None:
        # TODO Rewrite this
        mentionStr: str = ''
        for f in os.listdir('./data/userdata/'):
            u: User = User.get_by_id(int(f.removesuffix('.usv')))
            if not u.allowPing: continue
            # print(u.ID, [(t[0] < dt.now(t[0].tzinfo).timetz() < t[1]) for t in u.allowedPingTimes]) # remove only for testing
            if not any([(t[0] < dt.now(t[0].tzinfo).timetz() < t[1]) for t in u.allowedPingTimes]): continue
            mentionStr += str(u.getMentionStr())
        await ctx.respond(mentionStr + '\n' + message if len(
            mentionStr) > 0 else ctx.author.mention + ' no one to be pinged')  # type: ignore

    @lobbyPing.error  # type: ignore
    async def lobbyPingErr(self, ctx: discord.Message, error: discord.ApplicationCommandError) -> None:
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.respond("You don't have the permissions to use this command.", ephemeral=True)  # type: ignore
        if isinstance(error, (commands.CommandOnCooldown)):
            await ctx.respond(f"This command is on cool-down, come back in {round(error.retry_after, 2)} second(s)",
                              ephemeral=True)  # type: ignore
        elif error.__cause__.__class__ == UserDoesNotExist:
            await ctx.respond("User does not exist")  # type: ignore
        else:
            logger.error(error, stack_info=True)
            await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True)  # type: ignore


def setup(bot: discord.Bot) -> None:
    bot.add_cog(PingCog(bot))
