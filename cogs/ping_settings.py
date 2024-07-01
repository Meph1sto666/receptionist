from datetime import time  # type: ignore
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
        self.toggleBtn: discord.Button = discord.ui.Button(  # type: ignore
            style=discord.ButtonStyle.red if user.allow_ping else discord.ButtonStyle.green,
            label=f'(test)// {"disable" if user.allow_ping else "enable"} pings',
            custom_id='toggle_allow_ping',
        )
        self.addRuleBtn: discord.Button = discord.ui.Button(  # type: ignore
            style=discord.ButtonStyle.blurple,
            label=f'(test)// add time rule',
            custom_id='add_rule',
        )
        self.delRuleSelect: discord.SelectMenu = discord.ui.Select(  # type: ignore
            custom_id='del_rule_select',
            placeholder='delete ping rules',
            min_values=1,
            max_values=1,
            disabled=len(user.allowedPingTimes) < 1,
            options=self.getRulesOptions()
        )
        self.timezoneSelect: discord.SelectMenu = discord.ui.Select(  # type: ignore
            custom_id='timezone_select',
            placeholder='Select your timezone. If none is selected UTC will be used!',
            min_values=1,
            max_values=1,
            options=self.getTimezoneOptions()
        )
        self.toggleBtn.callback = self.toggle_allow_ping  # type: ignore
        self.addRuleBtn.callback = self.add_rule_modal  # type: ignore
        self.delRuleSelect.callback = self.del_rule_select  # type: ignore
        self.timezoneSelect.callback = self.tz_select_cb  # type: ignore
        for b in [self.toggleBtn, self.addRuleBtn, self.delRuleSelect, self.timezoneSelect]:  # type: ignore
            self.add_item(b)  # type: ignore

    async def del_rule_select(self, interaction: Interaction) -> None:
        """delete rule callback for select menu"""
        self.user.allowedPingTimes.remove(
            list(filter(lambda x: x[3] == interaction.data.get('values', [])[0], self.user.allowedPingTimes))[
                0])  # type: ignore
        self.delRuleSelect.options = self.getRulesOptions()
        if len(self.user.allowedPingTimes) < 1: self.delRuleSelect.disabled = True
        self.user.save()
        await interaction.response.edit_message(embed=generateRulesEmbedded(self.user), view=self)

    def getRulesOptions(self) -> list[discord.SelectOption]:
        """returns the options for the rule deletion select menu"""
        return [
            discord.SelectOption(
                label=f'(test)// Rule {i}',
                value=f'{self.user.allowedPingTimes[i][3]}',
                description=f'[Allow: {self.user.allowedPingTimes[i][2]}] / {self.user.allowedPingTimes[i][0]} - {self.user.allowedPingTimes[i][1]}'
            ) for i in range(len(self.user.allowedPingTimes))
        ] if len(self.user.allowedPingTimes) > 0 else [discord.SelectOption(label='None')]

    def getTimezoneOptions(self) -> list[discord.SelectOption]:
        return [
            discord.SelectOption(
                label='UTC' + (str(i) if str(i).startswith('-') and i != 0 else f'+{i}'),
                value=str(i),
                default=i == self.utcOffset
            ) for i in range(-12, 13)
        ]

    async def add_rule_modal(self, interaction: discord.Interaction) -> None:
        """callback for add rule modal button"""
        modal = PingRuleModal(parent=self, title='Ping Rules')
        await interaction.response.send_modal(modal)
        await modal.wait()

    # await interaction.response.edit_message(embed=generateRulesEmbedded(user), view=self)

    async def toggle_allow_ping(self, interaction: discord.Interaction) -> None:
        """callback to toggle if pinging the user is allowed"""
        self.user.allowPing = not self.user.allowPing
        self.toggleBtn.style = discord.ButtonStyle.red if self.user.allowPing else discord.ButtonStyle.green
        self.user.save()
        await interaction.response.edit_message(embed=generateRulesEmbedded(self.user), view=self)

    async def tz_select_cb(self, interaction: discord.Interaction) -> None:
        """callback to set the users timezone"""
        self.utcOffset = int(interaction.data.get('values', [])[0])
        self.timezoneSelect.options = self.getTimezoneOptions()
        await interaction.response.edit_message(embed=generateRulesEmbedded(self.user), view=self)


class PingRuleModal(discord.ui.Modal):
    def __init__(self, parent: PingSettingsView, *children: InputText, title: str, custom_id: str | None = None,
                 timeout: float | None = None) -> None:
        super().__init__(*children, title=title, custom_id=custom_id, timeout=timeout)
        self.parent: PingSettingsView = parent
        self.add_item(discord.ui.InputText(
            label='Rule start time',
            custom_id='rule_start_time',
            placeholder='Time in 24h format ie. 19:09',
            min_length=5,
            max_length=5,
            required=True
        ))
        self.add_item(discord.ui.InputText(
            label='Rule end time',
            custom_id='rule_end_time',
            placeholder='Time in 24h format ie. 21:30',
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
                tz: timezone = timezone(timedelta(hours=self.parent.utcOffset))
                now: dt = dt.now()
                times.append(
                    dt(now.year, now.month, now.day, *[int(ts) for ts in timeString.split(':')], tzinfo=tz).timetz())
            else:
                await interaction.response.defer()
                return
        self.parent.user.allowedPingTimes.append((times[0], times[1], True, dt.now().isoformat()))
        self.parent.user.save()
        self.parent.delRuleSelect.options = self.parent.getRulesOptions()
        await interaction.response.edit_message(embed=generateRulesEmbedded(self.parent.user), view=self.parent)


class PingSettingsCog(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        super().__init__()
        self.bot: discord.Bot = bot

    @discord.slash_command(name="ping_settings", description="settings for lobby pings")  # type: ignore
    @commands.has_any_role(*getRoles(["tester"]))
    async def lobbyPingSettings(self, ctx: discord.ApplicationContext) -> None:
        user: User = User.get_by_id(ctx.author.id)
        await ctx.respond(embed=generateRulesEmbedded(user), view=PingSettingsView(user),
                          ephemeral=True)  # type: ignore
        user.save()


def generateRulesEmbedded(user: User) -> discord.Embed:
    # user:User = loadUser(userId)
    emb: discord.Embed = discord.Embed(
        color=discord.colour.Color.from_rgb(*(0, 255, 0) if user.allowPing else (255, 0, 0)),
        title='(test)// ping rules',
        description='rules for incoming lobby ping requests. You can disable them or specify times to receive pings',
        timestamp=dt.now(),
        fields=[]
    )
    emb.set_footer(text=f'(test)// receive lobby pings: {user.allowPing}')
    for i in range(len(user.allowedPingTimes)):
        emb.add_field(
            name=f'(test)// Rule {i}',
            value=f'start: [{user.allowedPingTimes[i][0].isoformat()}]\nend: [{user.allowedPingTimes[i][1].isoformat()}]',
            inline=True
        )
    return emb


def setup(bot: discord.Bot) -> None:
    bot.add_cog(PingSettingsCog(bot))
