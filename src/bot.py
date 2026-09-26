import discord
from discord_control.commands import *
from discord import app_commands
import  os
from dotenv import load_dotenv

load_dotenv()

USER_COMMANDS = {
    "!join": join,
    "!leave": leave,
    "!play": play,
    "!search": search,
    "!skip": skip,
    "!stop": stop,
    "!pause": pause,
    "!resume": resume,
    "!playing": playing,
    "!queue": queue,
    "!parrot": parrot,
    "!playalbum": play_album,
    "!silent": silent,
    "!playrandomalbum": play_random_album,
    "!playrandom": play_random,
    "!remove": remove_item,
    "!clearqueue": clear_queue,
    "!shufflequeue": shuffle_queue,
    "!autoplay": autoplay
}

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.default()
        )

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if not message.content:
            return
        
        command = message.content.split()[0]
        if command in USER_COMMANDS:
            await USER_COMMANDS[command](message)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient()

@app_commands.command(name="join", description=f"Makes {client.user} join the current voice channel.")
async def join_command(interaction: discord.Interaction):
    await join(interaction)

client.run(os.getenv("DISCORD_BOT_TOKEN"))

"""
!lyrics
!albuminfo
!artistinfo
!help
"""