import discord
from navidrome.api import get_image

class PlayerControls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    def build_embed(self, guild):
        embed = discord.Embed(colour=0xdc8e10,title="**Currently Playing**", description=f"{guild.now_playing['title']}\nby {guild.now_playing['artist']}.")
        embed.set_thumbnail(url=guild.now_playing["cover_art_url"])
        return embed

    @discord.ui.button(label="⏮️", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import previous
        ctx = create_context(interaction)
        await previous(ctx)     

    @discord.ui.button(label="⏯️", style=discord.ButtonStyle.primary)
    async def play_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import resume, pause
        ctx = create_context(interaction)
        if ctx.voice.is_paused():
            await resume(ctx)
        else:
            await pause(ctx)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.primary)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import skip
        ctx = create_context(interaction)
        await skip(ctx)

    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.primary)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import stop
        ctx = create_context(interaction)
        await stop(ctx)
