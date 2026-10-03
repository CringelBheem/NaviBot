from navidrome.api import build_stream_url
import discord
from discord import FFmpegPCMAudio
from navidrome.api import search_random, get_image
import requests

def use_queue(voice, guild):
    if len(guild.queue) > 0:
        next_queue = guild.queue.pop()
        next_track = next_queue["id"]
        if guild.now_playing["track_id"]:
            guild.history.append(guild.now_playing.copy())
        guild.now_playing["title"] = next_queue["title"]
        guild.now_playing["artist"] = next_queue["artist"]
        guild.now_playing["track_id"] = next_queue["id"]
        cover_url = next_queue['cover_art_url']
        requests.get(cover_url)
        guild.now_playing["cover_art_url"] = cover_url
        #guild.now_playing["cover_art_url"]= next_queue['cover_art_url']
        guild.panel_change = True
        url = build_stream_url(next_track)         
        source = discord.FFmpegPCMAudio(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn")
        voice.play(source, after=lambda e:use_queue(voice, guild))
    else:
        if guild.autoplay == 1:
            randsong = search_random(1)
            if not randsong:
                return
            track = randsong[0]
            guild.queue.insert(0, {"id": track["id"], "title": track['title'], "artist": track['artist'], "cover_art_url": get_image(track['coverArt'])})
            use_queue(voice, guild)
        else:
            guild.now_playing["title"] = ""
            guild.now_playing["artist"]= ""
            guild.now_playing["track_id"]= ""
            guild.now_playing["cover_art"]= ""
            return

async def add_track(voice, respond, guild, track):
    track_id = track["id"]
    if not voice.is_playing() and not voice.is_paused():
        url = build_stream_url(track_id)       
        source = discord.FFmpegPCMAudio(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn")
        voice.play(source, after=lambda e:use_queue(voice, guild))
        if guild.now_playing["track_id"]:
            guild.history.append(guild.now_playing.copy())
        guild.now_playing["title"] = track['title']
        guild.now_playing["artist"] = track['artist']
        guild.now_playing["track_id"] = track_id
        cover_url = get_image(track['coverArt'])
        requests.get(cover_url)
        guild.now_playing["cover_art_url"]= cover_url
        guild.now_playing["cover_art_url"]= get_image(track['coverArt'])
        guild.panel_change = True
        if guild.silent == 0:
            await respond(f"Playing: {track['title']} by {track['artist']}")
    else:
        guild.queue.insert(0, {"id": track_id, "title": track['title'], "artist": track['artist'], "cover_art_url": get_image(track['coverArt'])})
        if guild.silent == 0:
            await respond(f"Added: {track['title']} by {track['artist']} to queue. Position: {len(guild.queue)}")
