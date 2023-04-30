from lib.types.faemuinvite import *
from lib.types.user import *

def createInviteEmbed(user:User) -> discord.Embed:
    embed = discord.Embed(
        color=discord.Color.from_rgb(255, 0, 255),
        title=user.language.translate("active_invite"),
        # description=user.language.translate("non_expired_invites"),
        timestamp=dt.now(),
        fields=[i.createEmbedField(user.language) for i in user.invites]
    )
    embed.set_footer(text="READ THE FUCKING GUIDE B****")
    return embed