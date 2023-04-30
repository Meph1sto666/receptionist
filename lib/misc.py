from lib.types.faemuinvite import *
from lib.types.user import *

def createInviteEmbed(user:User) -> discord.Embed:
    embed = discord.Embed(
        color=discord.Color.from_rgb(255, 0, 255),
        title="Your active Invites",
        description="The Invites that are not expired so far",
        timestamp=dt.now(),
        fields=[i.createEmbedField() for i in user.invites]
    )
    embed.set_footer(text="READ THE FUCKING GUIDE B****")
    return embed