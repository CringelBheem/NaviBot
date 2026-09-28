import discord
from discord_control.commands import *
from discord import app_commands
import  os
from dotenv import load_dotenv
from state import CommandContext, get_guild
from discord_control.responses import *
from discord_control.slash_commands import register

load_dotenv()

USER_COMMANDS = {
    "!join": join,
    "!leave": leave,
    #"!play": play,
    #"!search": search,
    "!skip": skip,
    "!stop": stop,
    "!pause": pause,
    "!resume": resume,
    "!playing": playing,
    "!queue": queue,
    "!parrot": parrot,
    #"!playalbum": play_album,
    "!silent": silent,
    "!playrandomalbum": play_random_album,
    #"!playrandom": play_random,
    #"!remove": remove_item,
    "!clearqueue": clear_queue,
    "!shufflequeue": shuffle_queue,
    "!autoplay": autoplay
}

class MyClient(discord.Client):
    def __init__(self):
        intents=discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        register(self.tree)
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        success = lambda: message.add_reaction("✅")
        failure = lambda : message.add_reaction("❌")
        ctx = CommandContext(guild_state= get_guild(message.guild.id), voice=message.guild.voice_client, respond=message.channel.send, success=success, failure=failure, user_voice=message.author.voice)
        if message.author == self.user:
            return
        
        if not message.content:
            return
        
        command = message.content.split()[0]
        if command == "!play":
            try:
                query = message.content.split(" ", 1)[1]
            except(IndexError, ValueError):
                await error_response("No songs found.", get_guild(message.guild.id), message.channel.send, failure)
                return
            await play(ctx, query)
        elif command == "!search":
            try:
                query = message.content.split(" ", 1)[1]
            except(IndexError, ValueError):
                await error_response("No results found.", get_guild(message.guild.id), message.channel.send, failure)
                return
            await search(ctx, query)
        elif command == "!playalbum":
            try:
                    query = message.content.split(" ", 1)[1]
            except(IndexError, ValueError):
                await error_response("No album found.", get_guild(message.guild.id), message.channel.send, failure)
                return
            await play_album(ctx, query)
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

client = MyClient()
client.run(os.getenv("DISCORD_BOT_TOKEN"))

"""
!lyrics
!albuminfo
!artistinfo
!help
"""