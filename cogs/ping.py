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
from lib.lang import Lang

logger: logging.Logger = logging.getLogger('bot')


class PingCog(commands.Cog):
	def __init__(self, bot: discord.Bot) -> None:
		super().__init__()
		self.bot: discord.Bot = bot

	@discord.slash_command(name="ping", description="pings for a lobby")  # type: ignore
	@commands.cooldown(1, 3600, type=commands.cooldowns.BucketType.guild)
	@commands.has_any_role(*getRoles(["tester"]))
	async def lobbyPing(self, ctx: discord.Message, message: str) -> None:
		mention_str: str = ''
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

			mention_str += str(usr.get_mention_str())
		max_mentions_per_msg:int = 95
		mention_str_len = 21
		mention_str_split:list[str] = [mention_str[i:i+max_mentions_per_msg*mention_str_len] for i in range(0, len(mention_str), max_mentions_per_msg*mention_str_len)]
		mention_str_split.append(message[:2000])

		await ctx.respond(mention_str_split[0] if len(mention_str) > 0 else Lang(User.get_or_create(id=ctx.author.id)[0].language).translate("cannot_ping_empty"), ephemeral=len(mention_str)<1)
		for msg in mention_str_split[1:]:
			await ctx.channel.send(msg)

	@lobbyPing.error  # type: ignore
	async def lobbyPingErr(self, ctx: discord.Message, error: discord.ApplicationCommandError) -> None:
		lang:Lang = Lang(User.get_or_create(id=ctx.author.id)[0].language)
		if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			await ctx.respond(lang.translate("missing_command_permission"), ephemeral=True)  # type: ignore
		if isinstance(error, (commands.CommandOnCooldown)):
			await ctx.respond(lang.translate("command_on_cooldown").format(t_in_m=round(error.retry_after/60, 2)), ephemeral=True)  # type: ignore
		elif error.__cause__.__class__ == UserDoesNotExist:
			await ctx.respond(lang.translate("user_does_not_exist"))  # type: ignore
		else:
			logger.error(error, stack_info=True)
			await ctx.respond(open("./data/errormessage.txt", encoding="utf-8").read(), ephemeral=True)  # type: ignore


def setup(bot: discord.Bot) -> None:
	bot.add_cog(PingCog(bot))
