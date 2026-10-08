import discord
from discord.ext import tasks
from state import guilds
from discord_control.ui_view import PlayerControls, QueueControls

@tasks.loop(seconds=0.3)
async def update_panels():
    for guild in guilds.values():
        if not guild.panel_change:
            continue

        if guild.queue_message:
            if not guild.queue_controls:
                guild.queue_controls = QueueControls()
            queue_view = guild.queue_controls
            queue_channel = guild.queue_message.channel
            try:
                await guild.queue_message.edit(embeds=queue_view.build_embed(guild), view=queue_view)
            except discord.errors.NotFound:
                guild.queue_message = None
        
        if guild.player_message:
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