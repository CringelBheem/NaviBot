import discord
from discord_control.commands import *
from discord import app_commands
import  os
from dotenv import load_dotenv
from state import CommandContext, get_guild
from discord_control.responses import *
from discord_control.slash_commands import register
from discord_control.prefix_commands import handle_prefix

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
        handle_prefix(self, message)

client = MyClient()
client.run(os.getenv("DISCORD_BOT_TOKEN"))

"""
!lyrics
!albuminfo
!artistinfo
!help
"""