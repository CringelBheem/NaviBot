from discord.ext import tasks
from state import guilds
from discord_control.ui_view import PlayerControls

@tasks.loop(seconds=0.3)
async def update_panels():
    for guild in guilds.values():
        if not guild.panel_change:
            continue

        if not guild.player_message:
            continue

        view = PlayerControls()
        await guild.player_message.edit(embed=view.build_embed(guild), view=view)
        guild.panel_change = False