import discord


class PlayerControls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label="previous", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, buttom: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import previous
        ctx = create_context(interaction)
        await previous(ctx)

    @discord.ui.button(label="Play/Pause", style=discord.ButtonStyle.primary)
    async def play_button(self, interaction: discord.Interaction, buttom: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import resume, pause
        ctx = create_context(interaction)
        if ctx.voice.is_paused():
            await resume(ctx)
        else:
            await pause(ctx)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.primary)
    async def skip_button(self, interaction: discord.Interaction, buttom: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import skip
        ctx = create_context(interaction)
        await skip(ctx)