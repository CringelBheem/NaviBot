from discord_control.commands import *


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
    "!playrandomalbum": play_random_album,
    "!clearqueue": clear_queue,
    "!shufflequeue": shuffle_queue,
    "!autoplay": autoplay,
    "!previous": previous
}

PARAM_COMMANDS = {
    "!play": play,
    "!search": search,
    #"!parrot": parrot,
    "!playalbum": play_album,
    #"!playrandom": play_random,
    #"!remove": remove_item
}

async def handle_prefix(self, message):
    success = lambda: message.add_reaction("✅")
    failure = lambda : message.add_reaction("❌")
    ctx = CommandContext(guild_state= get_guild(message.guild.id), voice=message.guild.voice_client, respond=message.channel.send, success=success, failure=failure, user_voice=message.author.voice)
    if message.author == self.user:
        return
    
    if not message.content:
        return
    
    command = message.content.split()[0]
    if command in PARAM_COMMANDS:
        try:
            query = message.content.split(" ", 1)[1]
        except(IndexError, ValueError):
            await error_response("No results found.", get_guild(message.guild.id), message.channel.send, failure)
            return
        await PARAM_COMMANDS[command](ctx, query)
    elif command == "!playrandom":
        try:
            size = int(message.content.split(" ", 1)[1])
        except (IndexError, ValueError):
            size = None
        await play_random(ctx, size)
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