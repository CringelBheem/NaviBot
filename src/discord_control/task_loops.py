import discord
from discord.ext import tasks
from state import guilds
from discord_control.ui_view import PlayerControls

@tasks.loop(seconds=2)
async def update_panels():
    for guild in guilds.values():
        if not guild.panel_change:
            continue

        if not guild.player_message:
            continue

        if not guild.player_controls:
            guild.player_controls = PlayerControls()
        
        view = guild.player_controls
        channel = guild.player_message.channel

        try:
            if guild.player_message:
                await guild.player_message.delete()
            guild.player_message = await channel.send(embed=view.build_embed(guild), view=view)
        except discord.errors.NotFound:
            guild.player_message = None
        guild.panel_change = False