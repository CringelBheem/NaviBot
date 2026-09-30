import discord
from discord_control.commands import skip
from discord_control.slash_commands import create_context

class PlayerControls(discord.ui.view):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label="Skip", style=discord.Button.primary)
    async def skip_buttom(self, interaction: discord.Interaction, buttom: discord.ui.Button):
        ctx = create_context(interaction)
        await skip(ctx)