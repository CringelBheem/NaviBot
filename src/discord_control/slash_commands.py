import discord
from discord import app_commands
from discord_control.commands import *
from state import CommandContext, get_guild
from navidrome.api import search_navidrome

async def do_nothing():
    pass


def create_context(interaction: discord.Interaction):

    async def respond(text):
        if not interaction.response.is_done():
            await interaction.response.send_message(text)
        else:
            await interaction.followup.send(text)
        

    return CommandContext(guild_state= get_guild(interaction.guild.id), voice=interaction.guild.voice_client, respond=respond, success = do_nothing, failure= do_nothing, user_voice=interaction.user.voice)

async def song_autocomplete(interaction: discord.Interaction, search: str):
    results = search_navidrome(search, "search2")
    songs = results.get("song", [])
    return [
        app_commands.Choice(name=f"{song['title'] - song['artist']}", value=song['title']) for song in songs[:25]
    ]

    


def register(tree):
    @tree.command(name="join", description=f"Makes the bot join the current voice channel.")
    async def join_command(interaction: discord.Interaction):
        await join(create_context(interaction))
    @tree.command(name="leave", description=f"Makes the bot leave the current voice channel.")
    async def leave_command(interaction: discord.Interaction):
        await leave(create_context(interaction))
    @tree.command(name="play", description=f"Adds a track for the bot to play.")
    @app_commands.autocomplete(query=song_autocomplete)
    async def play_command(interaction: discord.Interaction, query: str):
        await play(create_context(interaction), query)
    @tree.command(name="search", description=f"Searches navidrome for artists, albums, and songs.")
    async def search_command(interaction: discord.Interaction, query: str):
        await search(create_context(interaction), query)
    @tree.command(name="skip", description=f"Skips the current playing song.")
    async def skip_command(interaction: discord.Interaction):
        await skip(create_context(interaction))
    @tree.command(name="stop", description=f"Stops all songs.")
    async def stop_command(interaction: discord.Interaction):
        await stop(create_context(interaction))
    @tree.command(name="pause", description=f"Pauses the current playing song.")
    async def pause_command(interaction: discord.Interaction):
        await pause(create_context(interaction))
    @tree.command(name="resume", description=f"Resumes the current playing song.")
    async def resume_command(interaction: discord.Interaction):
        await resume(create_context(interaction))
    @tree.command(name="playing", description=f"Shows the currently playing song.")
    async def playing_command(interaction: discord.Interaction):
        await playing(create_context(interaction))    
    @tree.command(name="queue", description=f"Displays the queue.")
    async def queue_command(interaction: discord.Interaction):
        await queue(create_context(interaction))    
    @tree.command(name="play_album", description=f"Queues all songs in an album.")
    async def play_album_command(interaction: discord.Interaction, query: str):
        await play_album(create_context(interaction), query)
    @tree.command(name="silent", description=f"Toggles silent mode.")
    async def silent_command(interaction: discord.Interaction):
        await silent(create_context(interaction))    
    @tree.command(name="play_random_album", description=f"Queues all songs in a random album.")
    async def play_random_album_command(interaction: discord.Interaction):
        await play_random_album(create_context(interaction))
    @tree.command(name="play_random", description=f"Queues requested amount of random songs.")
    async def play_random_command(interaction: discord.Interaction, size: int):
        await play_random(create_context(interaction), size)
    @tree.command(name="remove", description=f"Removes an item at requested position within the queue.")
    async def remove_command(interaction: discord.Interaction, queue_ind: int):
        await remove_item(create_context(interaction), queue_ind)
    @tree.command(name="clear_queue", description=f"Removes all items in the queue.")
    async def clear_queue_command(interaction: discord.Interaction):
        await clear_queue(create_context(interaction))
    @tree.command(name="shuffle", description=f"Shuffles all items in the queue.")
    async def shuffle_command(interaction: discord.Interaction):
        await shuffle_queue(create_context(interaction))
    @tree.command(name="autoplay", description=f"Toggles autoplay.")
    async def autoplay_command(interaction: discord.Interaction):
        await autoplay(create_context(interaction))    
    
    