from datetime import datetime as dt
import os
import discord
from discord.ext import commands
from lib.roles import getRoles
from models import User
from lib.types.errors import UserDoesNotExist
import logging
from datetime import time
from datetime import timezone, timedelta
import pytz

logger: logging.Logger = logging.getLogger('bot')


class PingCog(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot

    @discord.slash_command(name="ping", description="pings for a lobby")  # type: ignore
    # @commands.cooldown(1, 3600, type=commands.cooldowns.BucketType.guild)
    @commands.has_any_role(*getRoles(["tester"]))
    async def lobbyPing(self, ctx: discord.Message, message: str) -> None:
        mentionStr: str = ''
        for usr in User.select():
            usr:User
            do_ping:bool = usr.allow_ping and len(usr.allowedPingTimes()) == 0 # if no rules and pings allowed ping
            for ping_rule in usr.allowedPingTimes():
                iso_utc:dt = dt.now(tz=pytz.utc)
                tz_offset = timezone(timedelta(minutes=usr.timezone))
                iso_start:dt = dt.combine(dt.date(iso_utc), time.fromisoformat(ping_rule.start), tzinfo=tz_offset)
                iso_end:dt = dt.combine(dt.date(iso_utc), time.fromisoformat(ping_rule.end), tzinfo=tz_offset)
                if iso_start > iso_end:
                    iso_end += timedelta(days=1)
                # print(f"START={iso_start}\tUTC={iso_utc}\tEND={iso_end}\tDO_PING={iso_start < iso_utc < iso_end}")
                do_ping = iso_start < iso_utc < iso_end
                if do_ping:
                    break
            if not do_ping:
                continue

            mentionStr += str(usr.get_mention_str())
        await ctx.respond(mentionStr + '\n' + message if len(mentionStr) > 0 else ctx.author.mention + ' no one to be pinged')  # type: ignore

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
