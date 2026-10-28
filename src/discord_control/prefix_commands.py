from discord_control.commands import *
import asyncio

USER_COMMANDS = {
    "!join": join,
    "!leave": leave,
    "!skip": skip,
    "!stop": stop,
    "!pause": pause,
    "!resume": resume,
    "!playing": playing,
    "!queue": queue,
    "!silent": silent,
    "!play_random_album": play_random_album,
    "!clear_queue": clear_queue,
    "!shuffle": shuffle_queue,
    "!autoplay": autoplay,
    "!previous": previous,
    "!lyrics": lyrics,
    "!help": help
}

PARAM_COMMANDS = {
    "!play": play,
    "!search": search,
    #"!parrot": parrot,
    "!play_album": play_album,
    "!create_playlist": add_playlist,
    "!search_playlist": search_playlist
    #"!playrandom": play_random,
    #"!remove": remove_item
}

async def handle_prefix(self, message):
    if message.author == self.user:
        return
    if not message.content:
        return    
    
    success = lambda: message.add_reaction("✅")
    failure = lambda : message.add_reaction("❌")
    guild = get_guild(message.guild.id)
    guild.loop = asyncio.get_running_loop()

    async def send_player_panel(**kwargs):
        return await message.channel.send(**kwargs)
    
    ctx = CommandContext(guild_state= guild, voice=message.guild.voice_client, respond=message.channel.send, success=success, failure=failure, user_voice=message.author.voice, send_player_panel=send_player_panel)
    
    command = message.content.split()[0]
    if command in PARAM_COMMANDS:
        try:
            query = message.content.split(" ", 1)[1]
        except(IndexError, ValueError):
            await error_response("No results found.", get_guild(message.guild.id), message.channel.send, failure)
            return
        await PARAM_COMMANDS[command](ctx, query)
    elif command == "!play_random":
        try:
            size = int(message.content.split(" ", 1)[1])
        except (IndexError, ValueError):
            size = None
        await play_random(ctx, size)
    elif command == "!add_to_playlist":
        try:
            split = (message.content.split(" ", 2))
            playlist = split[1]
            track = split[2]
        except (IndexError, ValueError):
            await error_response("No valid playlist or track.", get_guild(message.guild.id), message.channel.send, failure)
            return
        await add_track_to_playlist(ctx, playlist, track)
    elif command == "!remove":
        try:
            queue_ind = int(message.content.split(" ", 1)[1])
        except (IndexError, ValueError):
            await error_response("No valid index.", get_guild(message.guild.id), message.channel.send, failure)
            return
        await remove_item(ctx, queue_ind)
    elif command == "!parrot":
        try:
            parrot_text = message.content[8:]
        except (IndexError, ValueError):
            await error_response("No text.", get_guild(message.guild.id), message.channel.send, failure)
            return
        await parrot(ctx, parrot_text)
    elif command in USER_COMMANDS:
        await USER_COMMANDS[command](ctx)