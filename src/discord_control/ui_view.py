import discord


class PlayerControls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.primary)
    async def skip_button(self, interaction: discord.Interaction, buttom: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import skip
        ctx = create_context(interaction)
        await skip(ctx)