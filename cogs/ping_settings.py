from datetime import date, time  # type: ignore
from datetime import datetime as dt
import re
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui.input_text import InputText
from discord.ui.item import Item
from lib.roles import getRoles
from models import User
import logging
from datetime import timezone, timedelta
import datetime
from models import *

logger: logging.Logger = logging.getLogger('bot')


class PingSettingsView(discord.ui.View):
    """
	modal for adding ping rules
	"""

    def __init__(self, user: User, *items: Item, timeout: float | None = 180,
                 disable_on_timeout: bool = False) -> None:  # type: ignore
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)  # type: ignore
        self.user: User = user
        self.utcOffset: int = 0
        self.lang = Lang(self.user.language)
        self.toggleBtn: discord.Button = discord.ui.Button(  # type: ignore
            style=discord.ButtonStyle.red if user.allow_ping else discord.ButtonStyle.green,
            label=self.lang.translate("disable_pings" if user.allow_ping else "enable_pings"),
            custom_id='toggle_allow_ping',
        )
        self.addRuleBtn: discord.Button = discord.ui.Button(  # type: ignore
            style=discord.ButtonStyle.blurple,
            label=self.lang.translate("add_ping_rule"),
            custom_id='add_rule',
        )
        self.delRuleSelect: discord.SelectMenu = discord.ui.Select(  # type: ignore
            custom_id='del_rule_select',
            placeholder=self.lang.translate("delete_ping_rule"),
            min_values=1,
            max_values=1,
            disabled=len(user.allowedPingTimes()) < 1,
            options=self.getRulesOptions()
        )
        self.toggleBtn.callback = self.toggle_allow_ping  # type: ignore
        self.addRuleBtn.callback = self.add_rule_modal  # type: ignore
        self.delRuleSelect.callback = self.del_rule_select  # type: ignore
        for b in [self.toggleBtn, self.addRuleBtn, self.delRuleSelect]:#, self.timezoneSelect  # type: ignore
            self.add_item(b)  # type: ignore

    async def del_rule_select(self, interaction: Interaction) -> None:
        """delete rule callback for select menu"""
        PingRule.delete_by_id(interaction.data.get('values', [])[0])
        self.delRuleSelect.options = self.getRulesOptions()
        if len(self.user.allowedPingTimes()) < 1: self.delRuleSelect.disabled = True
        await interaction.response.edit_message(embed=generateRulesEmbedded(self.user), view=self)

    def getRulesOptions(self) -> list[discord.SelectOption]:
        """returns the options for the rule deletion select menu"""
        rules:list[PingRule] = self.user.allowedPingTimes()
        return [
            discord.SelectOption(
                label=self.lang.translate("rule_plus_id").format(n=i, id=rules[i].id),
                value=f'{rules[i].id}',
                description=f'[Allow: {rules[i].start} - {rules[i].end}' # TODO: add language support
            ) for i in range(len(rules))
        ] if len(rules) > 0 else [discord.SelectOption(label='None')]

    async def add_rule_modal(self, interaction: discord.Interaction) -> None:
        """callback for add rule modal button"""
        modal = PingRuleModal(parent=self, title=self.lang.translate("add_ping_rule"))
        await interaction.response.send_modal(modal)
        await modal.wait()

    async def toggle_allow_ping(self, interaction: discord.Interaction) -> None:
        """callback to toggle if pinging the user is allowed"""
        self.user.allow_ping = not self.user.allow_ping
        self.toggleBtn.style = discord.ButtonStyle.red if self.user.allow_ping else discord.ButtonStyle.green
        self.toggleBtn.label = self.lang.translate("disable_pings" if self.user.allow_ping else "enable_pings")
        self.user.save()
        await interaction.response.edit_message(embed=generateRulesEmbedded(self.user), view=self)


class PingRuleModal(discord.ui.Modal):
    def __init__(self, parent: PingSettingsView, *children: InputText, title: str, custom_id: str | None = None,
                 timeout: float | None = None) -> None:
        super().__init__(*children, title=title, custom_id=custom_id, timeout=timeout)
        self.parent: PingSettingsView = parent
        self.add_item(discord.ui.InputText(
            label=self.parent.lang.translate("rule_start_time"),
            custom_id='rule_start_time',
            placeholder=self.parent.lang.translate("ping_rule_modal_start_example").format(hh=str(random.randint(0,23)).rjust(2,"0"),mm=str(random.randint(0,60)).rjust(2,"0")),
            min_length=5,
            max_length=5,
            required=True
        ))
        self.add_item(discord.ui.InputText(
            label=self.parent.lang.translate("rule_end_time"),
            custom_id='rule_end_time',
            placeholder=self.parent.lang.translate("ping_rule_modal_end_example").format(hh=str(random.randint(0,23)).rjust(2,"0"),mm=str(random.randint(0,60)).rjust(2,"0")),
            min_length=5,
            max_length=5,
            required=True
        ))
        self.callback = self.cb

    async def cb(self, interaction: Interaction) -> None:
        components: list[dict[str, list[dict[str, str]]]] = interaction.data.get('components')  # type: ignore
        times: list[time] = []
        for c in components[:2]:
            comp: list[dict[str, str]] | None = c.get('components')
            timeString: str = comp[0].get('value')  # type: ignore
            if re.match(r'([0-1]\d|2[0-3]):[0-6]\d', timeString) is not None:
                # tz: timezone = timezone(timedelta(hours=self.parent.utcOffset))
                # now: dt = dt.now()
                times.append(time(*[int(ts) for ts in timeString.split(':')], tzinfo=None))
                    # dt(now.year, now.month, now.day, *[int(ts) for ts in timeString.split(':')], tzinfo=tz).timetz())
                    # dt(now.year, now.month, now.day, *[int(ts) for ts in timeString.split(':')], tzinfo=None).timetz())
            else:
                await interaction.response.defer()
                return
        # print(times)
        pr:PingRule = PingRule.create(start=times[0], end=times[1], creation_time=dt.now().isoformat(), user_id=interaction.user.id)
        pr.save(force_insert=False)
        self.parent.delRuleSelect.disabled = False
        self.parent.delRuleSelect.options = self.parent.getRulesOptions()
        await interaction.response.edit_message(embed=generateRulesEmbedded(self.parent.user), view=self.parent)


class PingSettingsCog(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot

    @discord.slash_command(name="ping_settings", description="settings for lobby pings")  # type: ignore
    @commands.has_any_role(*getRoles(["tester"]))
    async def lobbyPingSettings(self, ctx: discord.ApplicationContext) -> None:
        user: User = User.get_or_create(id=ctx.author.id)[0]
        await ctx.respond(embed=generateRulesEmbedded(user), view=PingSettingsView(user),
                          ephemeral=True)  # type: ignore
        user.save()


def generateRulesEmbedded(user: User) -> discord.Embed:
    lang:Lang=Lang(user.language)
    emb: discord.Embed = discord.Embed(
        color=discord.colour.Color.from_rgb(*(0, 255, 0) if user.allow_ping else (255, 0, 0)),
        title=lang.translate("ping_settings_embed_title"),
        description=lang.translate("ping_settings_embed_desc"),
        timestamp=dt.now(),
        fields=[]
    )
    emb.set_footer(text=lang.translate("ping_settings_embed_footer").format(allow_pings=user.allow_ping))
    rules:list[PingRule]= user.allowedPingTimes()
    user_today_date:date = dt.now(timezone(timedelta(minutes=user.timezone))).date()
    for i in range(len(rules)):
        iso_time_start:str = f"<t:{round(dt.combine(user_today_date, time.fromisoformat(rules[i].start)).timestamp())}:t>"
        iso_time_end:str = f"<t:{round(dt.combine(user_today_date, time.fromisoformat(rules[i].end)).timestamp())}:t>"
        emb.add_field(
            name=lang.translate("rule_plus_id").format(n=i, id=rules[i].id),
            value=lang.translate("ping_settings_embed_field_value").format(start_time=iso_time_start, end_time=iso_time_end),
            # value=f'start: [{rules[i].start}]\nend: [{rules[i].end}]',
            inline=True
        )
    return emb


def setup(bot: discord.Bot) -> None:
    bot.add_cog(PingSettingsCog(bot))
