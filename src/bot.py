import discord
from discord_control.commands import *
from discord import app_commands
import  os
from dotenv import load_dotenv
from discord_control.responses import *
from discord_control.slash_commands import register
from discord_control.prefix_commands import handle_prefix
from discord_control.task_loops import update_panels, update_lyrics

load_dotenv()

class MyClient(discord.Client):
    def __init__(self):
        intents=discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        register(self.tree)
        update_panels.start()
        update_lyrics.start()
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        await handle_prefix(self, message)

client = MyClient()
client.run(os.getenv("DISCORD_BOT_TOKEN"))


"""
!lyrics -> Run time and lyric array syncing needed.
!albuminfo -> Api call, possibly not useful.
!artistinfo -> Same as album info.
!help -> Returns an embedded message with each command.
Fix paused time so it add to a total, only reset when the song is over.
Fix non-synced lyrics returns so they still work.
"""