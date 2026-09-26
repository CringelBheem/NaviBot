from discord import app_commands

@app_commands.command(name="join", description=f"Makes {client.user} join the current voice channel.")
async def join_command(interaction: discord.Interaction):
    await join(interaction)
