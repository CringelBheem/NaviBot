from state import get_guild, CommandContext
import discord
from discord_control.responses import silent_response, error_response, join_check
from music.player import add_track, play_now
from navidrome.api import search_navidrome, search_album, search_random, get_lyrics, create_playlist, add_to_playlist, get_playlist_id, get_playlist
import random
from discord_control.ui_view import PlayerControls, QueueControls, SearchResult, LyricsResult, HelpResult
import time

async def join(ctx: CommandContext):
    if not ctx.voice:
        voice = await join_check(ctx)

        if not voice:
            return
        
    await silent_response(ctx.guild_state, ctx.success)

async def leave(ctx: CommandContext):
    guild = ctx.guild_state
    guild.now_playing["title"] = ""
    guild.now_playing["artist"]= ""
    guild.now_playing["track_id"]= ""
    guild.now_playing["cover_art"]= ""
    if guild.queue:
        guild.queue.clear()
    if ctx.voice:
        await ctx.voice.disconnect()
        if guild.silent == 0:
            await ctx.respond("Left the voice channel.")
    await silent_response(ctx.guild_state, ctx.success)
    
async def play(ctx: CommandContext, query: str):
    guild = ctx.guild_state
    if ctx.voice:
        voice = ctx.voice
    else:
        voice = await join_check(ctx)
    if not voice:
        return
    
    results = search_navidrome(query, "search2")
    songs = results.get("song", [])

    if not songs:
        await error_response("No songs found.", guild, ctx.respond, ctx.failure)
        return

    track = songs[0]
    await add_track(voice, ctx.respond, guild, track)
    await silent_response(ctx.guild_state, ctx.success)
        
async def search(ctx: CommandContext, query):
    guild = ctx.guild_state

    results = search_navidrome(query, "search2")
    artists = [a["name"] for a in results.get("artist", [])]
    artists_ids = [a["id"] for a in results.get("artist", [])]
    albums = [a["name"] for a in results.get("album", [])]
    albums_ids = [a["id"] for a in results.get("album", [])]
    songs = [s["title"] for s in results.get("song", [])]
    songs_ids = [s["id"] for s in results.get("song", [])]
    results = artists[:10] + albums[:10] + songs[:10]
    results_id = artists_ids[:10] + albums_ids[:10] + songs_ids[:10]
    """if len(artists) > 0:
        reply += "\n**Artists: **\n"
        for artist in artists:
            reply += f" - {artist}\n"
    if len(albums) > 0:
        reply += "\n**Albums: **\n"
        for album in albums:
            reply += f" - {album}\n"
    if len(songs) > 0:
        reply += "\n**Songs: **\n"
        for song in songs[:10]:
            reply += f" - {song}\n"
    if not reply:"""
    view = SearchResult(results, results_id)
    embed = view.build_embed(guild, artists, albums, songs)
    if not embed:
        await error_response("No results found.", guild, ctx.respond, ctx.failure)
    else:
        await ctx.send_player_panel(embed=embed, view=view)

async def skip(ctx: CommandContext):
    guild = ctx.guild_state
    if guild.silent == 0:
        await ctx.respond(f"Skipping track.")
    voice = ctx.voice
    if voice:
        voice.stop()
    await silent_response(ctx.guild_state, ctx.success)
    
async def stop(ctx: CommandContext):
    guild = ctx.guild_state
    if guild.silent == 0:
        await ctx.respond(f"Stopped all songs.")
    if guild.queue:
        guild.queue.clear()
    guild.autoplay = 0
    voice = ctx.voice
    if voice:
        voice.stop()
    await silent_response(ctx.guild_state, ctx.success)

async def pause(ctx: CommandContext):
    guild = ctx.guild_state
    if guild.silent == 0:
        await ctx.respond(f"Paused.")
    voice = ctx.voice
    if not voice.is_paused():
        if voice:
            voice.pause()
            guild.pause_start = time.time()
    await silent_response(ctx.guild_state, ctx.success)

async def resume(ctx: CommandContext):
    guild = ctx.guild_state
    if guild.silent == 0:
        await ctx.respond(f"Resuming.")
    voice = ctx.voice
    if voice.is_paused():
        if voice:
            voice.resume()
            guild.paused_seconds += time.time() - guild.pause_start
            guild.pause_start = 0
    await silent_response(ctx.guild_state, ctx.success)

async def playing(ctx: CommandContext):
    guild = ctx.guild_state
    if not guild.player_controls:
        guild.player_controls = PlayerControls()
    
    view = guild.player_controls
    if (not guild.now_playing or guild.now_playing["title"] == ""):
        await ctx.respond("Nothing is currently playing.")
        return
    if guild.player_message:
        try:
            await guild.player_message.delete()
        except discord.NotFound:
            pass
    guild.player_message = await ctx.send_player_panel(embed=view.build_embed(guild), view=view)

async def queue(ctx: CommandContext):
    guild = ctx.guild_state
    if not guild.queue_controls:
        guild.queue_controls = QueueControls()
    view = guild.queue_controls
    if (not guild.now_playing or guild.now_playing["title"] == ""):
        await ctx.respond("Nothing is currently playing.")
        return
    if guild.queue_message:
        try:
            await guild.queue_message.delete()
        except discord.NotFound:
            pass
    guild.queue_controls.refresh_buttons(guild)    
    guild.queue_message = await ctx.send_player_panel(embeds=view.build_embed(guild), view=view)


    """
    if (not guild.now_playing or guild.now_playing["title"] == ""):
        await ctx.respond("Nothing is currently playing.")
        return
    reply = f"**Currently playing: ** {guild.now_playing['title']} by {guild.now_playing['artist']}.\n"
    for i, track in enumerate(reversed(guild.queue)):
        reply += f"**{i+1}: ** {track['title']} by {track['artist']}.\n"
    await ctx.respond(reply)
    """

async def parrot(ctx: CommandContext, parrot_text):
    await ctx.respond(parrot_text)
    #await message.delete()

async def play_album(ctx: CommandContext, query):
    guild = ctx.guild_state

    if ctx.voice:
        voice = ctx.voice
    else:
        voice = await join_check(ctx)

    if not voice:
        return
    
    songs = search_album(query)

    if not songs:
        await error_response("No albums found.", guild, ctx.respond, ctx.failure)
        return
    
    for track in songs:
        await add_track(voice, ctx.respond, guild, track)
    await silent_response(ctx.guild_state, ctx.success)

async def silent(ctx: CommandContext):
    guild = ctx.guild_state
    if guild.silent == 1:
        guild.silent = 0
        await ctx.success()
        await ctx.respond(f"Silent mode off.")
    else:
        guild.silent = 1
        await ctx.success()
        return

async def play_random_album(ctx: CommandContext):
    guild = ctx.guild_state

    if ctx.voice:
        voice = ctx.voice
    else:
        voice = await join_check(ctx)

    if not voice:
        return
    
    randsong = search_random(1)

    if not randsong:
        await error_response("No albums found.", guild, ctx.respond, ctx.failure)
        return
    
    album = randsong[0]["album"]

    songs = search_album(album)

    if not songs:
        await error_response("No songs found.", guild, ctx.respond, ctx.failure)
        return
    
    for track in songs:
        await add_track(voice, ctx.respond, guild, track)
    await silent_response(ctx.guild_state, ctx.success)

async def play_random(ctx: CommandContext, size):
    guild = ctx.guild_state

    if ctx.voice:
        voice = ctx.voice
    else:
        voice = await join_check(ctx)

    if not voice:
        return
    
    songs = search_random(size)

    if not songs:
        await error_response("No songs found.", guild, ctx.respond, ctx.failure)
        return
    
    for track in songs:
        await add_track(voice, ctx.respond, guild, track)
    await silent_response(ctx.guild_state, ctx.success)

async def remove_item(ctx: CommandContext, queue_ind):
    guild = ctx.guild_state

    length = len(guild.queue)
    if 0 < queue_ind >= (length + 1):
        await error_response("No valid index.", guild, ctx.respond, ctx.failure)
        return
    try:
        removed_item = guild.queue.pop(length - queue_ind)
        if guild.silent == 0:
            await ctx.respond(f"Removed: {removed_item['title']} by {removed_item['artist']} from queue.")
        else:
            await silent_response(ctx.guild_state, ctx.success)
    except  (IndexError, ValueError):
        await error_response("No valid index.", guild, ctx.respond, ctx.failure)
        return

async def clear_queue(ctx: CommandContext):
    guild = ctx.guild_state
    if guild.queue:
        guild.queue.clear()
    if guild.silent == 0:
            await ctx.respond(f"Cleared queue.")
    await silent_response(ctx.guild_state, ctx.success)

async def shuffle_queue(ctx: CommandContext):
    guild = ctx.guild_state
    if guild.queue:
        random.shuffle(guild.queue)
    if guild.silent == 0:
            await ctx.respond(f"Shuffled queue.")
    await silent_response(ctx.guild_state, ctx.success)

async def autoplay(ctx: CommandContext):
    guild = ctx.guild_state
    if guild.autoplay == 0:
        guild.autoplay = 1
        if guild.silent == 0:
            await ctx.respond(f"Autoplay enabled.")
    else:
        guild.autoplay = 0
        if guild.silent == 0:
            await ctx.respond(f"Autoplay disabled.")
    await silent_response(ctx.guild_state, ctx.success)

async def previous(ctx: CommandContext):
    guild = ctx.guild_state
    
    voice = ctx.voice
    if guild.history:
        last_track = guild.history.pop()
        track = guild.now_playing
        if guild.silent == 0:
            await ctx.respond(f"Playing previous track.")
    else:
        await error_response("No previous track.", guild, ctx.respond, ctx.failure)
        return


    if voice:
        guild.pressed_previous = True
        guild.queue.append({"id": track["track_id"], "title": track['title'], "artist": track['artist'], "cover_art_url": track['cover_art_url']})
        guild.now_playing = last_track.copy()
        voice.stop()
        await play_now(voice, guild, last_track)


    await silent_response(ctx.guild_state, ctx.success)

async def lyrics(ctx: CommandContext):
    guild = ctx.guild_state
    song = guild.now_playing["track_id"]
    #get the runtime of song
    #add all lyrics less than that to an embed
    #when time of next line is reached, edit embed with new line
    song_lyrics = guild.lyrics
    """if not song_lyrics:
        await error_response("No lyrics found.", guild, ctx.respond, ctx.failure)
        return"""
    if guild.lyric_message:
        guild.lyric_message = None
    guild.lyrics_result = LyricsResult()
    embed = guild.lyrics_result.build_embed(song_lyrics, guild)
    if not embed:
        await error_response("No lyrics found.", guild, ctx.respond, ctx.failure)
    else:
        guild.lyric_message = await ctx.send_player_panel(embed=embed, view=guild.lyrics_result)

async def help(ctx: CommandContext):
    guild = ctx.guild_state
    view = HelpResult()
    embed = view.build_embed()
    if not embed:
        await error_response("A problem has occurred while fetching help.", guild, ctx.respond, ctx.failure)
    else:
        await ctx.send_player_panel(embed=embed, view=view)

async def add_playlist(ctx: CommandContext, name):
    guild = ctx.guild_state
    id = create_playlist(name)
    if id:
        if guild.silent == 0:
            await ctx.respond(f"Created playlist: {name}\nId: {id}")
        else:
            await silent_response(guild, ctx.success)

async def add_track_to_playlist(ctx: CommandContext, playlist, track):
    guild = ctx.guild_state
    id = get_playlist_id(playlist)
    if not id:
        await error_response("No playlist found.", guild, ctx.respond, ctx.failure)
        return
    results = search_navidrome(track, "search2")
    songs = results.get("song", [])
    if not songs:
        await error_response("No tracks found.", guild, ctx.respond, ctx.failure)
        return
    track_id = songs[0]["id"]
    status = add_to_playlist(id, track_id)
    if status == "ok":
        if guild.silent == 0:
            await ctx.respond(f"Added {track} to {playlist}.")
        else:
            await silent_response(guild, ctx.success)
    else:
        await error_response("No tracks found.", guild, ctx.respond, ctx.failure)
        return

async def search_playlist(ctx: CommandContext, playlist):
    guild = ctx.guild_state
    id = get_playlist_id(playlist)
    results = get_playlist(id)
    if not results:
        await error_response("No playlist found.", guild, ctx.respond, ctx.failure)
        return
    songs = [s["title"] for s in results]
    songs_ids = [s["id"] for s in results]
    view = SearchResult(songs, songs_ids)
    embed = view.build_embed(guild, [], [], songs)
    if not embed:
        await error_response("No results found.", guild, ctx.respond, ctx.failure)
    else:
        await ctx.send_player_panel(embed=embed, view=view)


async def play_playlist(ctx: CommandContext, playlist):
    guild = ctx.guild_state
    id = get_playlist_id(playlist)
    songs = get_playlist(id)
    if ctx.voice:
        voice = ctx.voice
    else:
        voice = await join_check(ctx)

    if not voice:
        return
    
    #songs = [s["title"] for s in results]

    if not songs:
        await error_response("No playlists found.", guild, ctx.respond, ctx.failure)
        return
    
    for track in songs:
        await add_track(voice, ctx.respond, guild, track)
    await silent_response(ctx.guild_state, ctx.success)