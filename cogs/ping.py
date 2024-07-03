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
            if not usr.allow_ping: continue
            # print(u.ID, [(t[0] < dt.now(t[0].tzinfo).timetz() < t[1]) for t in u.allowedPingTimes]) # remove only for testing

            do_ping:bool = False
            for ping_rule in usr.allowedPingTimes():
                iso_start:time = time.fromisoformat(ping_rule.start)
                iso_end:time = time.fromisoformat(ping_rule.end)

                iso_hours = int(timedelta(minutes=usr.timezone).total_seconds() / 60 / 60)

                offset = int(str(iso_hours).split(":")[0])

                utc_now = dt.now()

                now_h = utc_now.hour + offset
                if len(str(now_h)) == 1:
                    now_h = f'0{now_h}'
                now_m = utc_now.minute
                if len(str(now_m)) == 1:
                    now_m = f'0{now_m}'
                now_s = utc_now.second
                if len(str(now_s)) == 1:
                    now_s = f'0{now_s}'

                
                do_ping = iso_start < time.fromisoformat(f'{now_h}:{now_m}:{now_s}') < iso_end

                if do_ping:
                    break

                # tz_offset = timezone(timedelta(minutes=-usr.timezone)) # <-- you mean this one?
                
                # now:dt = dt.now(tz=pytz.utc)

                # start = dt(now.year, now.month, now.day, iso_start.hour, iso_start.minute, tzinfo=tz_offset)
                # end = dt(now.year, now.month, now.day + (1 if iso_start>iso_end else 0), iso_end.hour, iso_end.minute, tzinfo=tz_offset) # This should in theory advance the end time by one day if the end time is smaller like 23:00 to 00:02
                
                # print(f'iso_start={iso_start}\tiso_end={iso_end}\tTZ={tz_offset}\tNow={now}\tStart={start}\tEnd={end}')
                # # dt.now(tz) == returns in the wrong TZ. always seems to use UTC instead of the provided TZ
                # print(f'Start={start}\tNow({pytz.utc})={now}\tEnd={end}\t\t\tdo_ping={start < dt.now(tz_offset) < end}') # now should be correct tho no?
                
                # print(f"POSX {start} < dt.now(tz) < end")
                #   so UTC+2 10:00 to UTC+2 12:00 = ping_rule
                #   start and end will match 10:00 - 12:00
                # 
                #
                # now Now is the users time at 11:22 if you want UTC then just give it pytz.utc as timezone
                # _start:time = time.fromisoformat(ping_rule.start)
                # tz = timezone(timedelta(minutes=-usr.timezone))
                # now:dt = dt.now()
                # start = dt(now.year, now.month, now.day, _start.hour, _start.minute, tzinfo=tz).timestamp()
                # _end:time = time.fromisoformat(ping_rule.end)
                # end = dt(now.year, now.month, now.day, _end.hour, _end.minute, tzinfo=tz).timestamp()
                # print(start, dt.now(tz.utc).timestamp(), end, "|", start < dt.now(tz.utc).timestamp(), dt.now(tz.utc).timestamp() < end)
                # if start < dt.now(tz.utc).timestamp() < end:
                #     do_ping = True
                #     break
            if not do_ping: continue

            # print(dt.time(dt.strptime(u.allowedPingTimes()[0].start, "%H:%M:%S%z")))
            # print(dt.time(dt.strptime(t.start, "%H:%M:%S%z")))
            # if not any([(time.strftime(t.start, "%H:%M:%S%z") < dt.now(t.start.tzinfo).timetz() < t.end) for t in u.allowedPingTimes()]): continue
            mentionStr += str(usr.get_mention_str())
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
