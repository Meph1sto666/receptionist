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
        for u in User.select():
            u:User
            if not u.allow_ping: continue
            # print(u.ID, [(t[0] < dt.now(t[0].tzinfo).timetz() < t[1]) for t in u.allowedPingTimes]) # remove only for testing

            do_ping:bool = False
            for t in u.allowedPingTimes():
                _start:time = time.fromisoformat(t.start)
                tz = timezone(timedelta(minutes=-u.timezone))
                now:dt = dt.now()
                start = dt(now.year, now.month, now.day, _start.hour, _start.minute, tzinfo=tz).timestamp()
                _end:time = time.fromisoformat(t.end)
                end = dt(now.year, now.month, now.day, _end.hour, _end.minute, tzinfo=tz).timestamp()
                print(start, dt.now(tz.utc).timestamp(), end, "|", start < dt.now(tz.utc).timestamp(), dt.now(tz.utc).timestamp() < end)
                if start < dt.now(tz.utc).timestamp() < end:
                    do_ping = True
                    break
            if not do_ping: continue

            # print(dt.time(dt.strptime(u.allowedPingTimes()[0].start, "%H:%M:%S%z")))
            # print(dt.time(dt.strptime(t.start, "%H:%M:%S%z")))
            # if not any([(time.strftime(t.start, "%H:%M:%S%z") < dt.now(t.start.tzinfo).timetz() < t.end) for t in u.allowedPingTimes()]): continue
            mentionStr += str(u.get_mention_str())
        await ctx.respond(mentionStr + '\n' + message if len(mentionStr) > 0 else ctx.author.mention + ' no one to be pinged')  # type: ignore

    @lobbyPing.error  # type: ignore
    async def lobbyPingErr(self, ctx: discord.Message, error: discord.ApplicationCommandError) -> None:
        raise
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
