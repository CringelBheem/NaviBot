import discord
from discord.ext import tasks
from state import guilds
from discord_control.ui_view import PlayerControls, QueueControls, LyricsResult
import time

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
                if guild.queue_message:
                    await guild.queue_message.delete()
                guild.queue_controls.refresh_buttons(guild)
                guild.queue_message = await queue_channel.send(embeds=queue_view.build_embed(guild), view=queue_view)
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


@tasks.loop(seconds=0.2)
async def update_lyrics():
    for guild in guilds.values():
        if guild.lyric_message:
            voice = guild.voice
            if voice and voice.is_paused():
                current_time = (guild.pause_start - guild.start_time - guild.paused_seconds) * 1000
            else:
                current_time = (time.time() - guild.start_time - guild.paused_seconds) * 1000
            new_index = 0
            for i, lyric in enumerate(guild.lyrics):
                if lyric["start"] < current_time:
                    new_index = i
                else:
                    break

            if new_index > guild.current_lyric_index:
                guild.current_lyric_index = new_index
                guild.update_lyrics = True

            if not guild.update_lyrics:
                continue
            
            if not guild.lyrics_result:
                guild.lyrics_result = LyricsResult()
            lyric_view = guild.lyrics_result
            try:
                await guild.lyric_message.edit(embed=lyric_view.build_embed(guild.lyrics, guild), view=lyric_view)
            except discord.errors.NotFound:
                guild.lyric_message = None

            guild.update_lyrics = False