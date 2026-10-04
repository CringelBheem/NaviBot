import discord
from state import get_guild

class PlayerControls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)

    def build_embed(self, guild):
        embed = discord.Embed(colour=0xdc8e10,title="**Currently Playing**", description=f"{guild.now_playing['title']}\nby {guild.now_playing['artist']}.")
        embed.set_thumbnail(url=guild.now_playing["cover_art_url"])
        return embed

    @discord.ui.button(emoji="⏮️", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import previous
        ctx = create_context(interaction)
        if not ctx.guild_state.silent:
            ctx.guild_state.silent = 1
            await previous(ctx)
            ctx.guild_state.silent = 0
        else:
            await previous(ctx)

    @discord.ui.button(emoji="⏯️", style=discord.ButtonStyle.primary)
    async def play_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import resume, pause
        ctx = create_context(interaction)
        if ctx.voice.is_paused():
            if not ctx.guild_state.silent:
                ctx.guild_state.silent = 1
                await resume(ctx)
                ctx.guild_state.silent = 0
            else:
                await resume(ctx)
        else:
            if not ctx.guild_state.silent:
                ctx.guild_state.silent = 1
                await pause(ctx)
                ctx.guild_state.silent = 0
            else:
                await pause(ctx)

    @discord.ui.button(emoji="⏭️", style=discord.ButtonStyle.primary)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import skip
        ctx = create_context(interaction)
        if not ctx.guild_state.silent:
            ctx.guild_state.silent = 1
            await skip(ctx)
            ctx.guild_state.silent = 0
        else:
            await skip(ctx)

    @discord.ui.button(emoji="⏹️", style=discord.ButtonStyle.primary)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from discord_control.slash_commands import create_context
        from discord_control.commands import stop
        ctx = create_context(interaction)
        if not ctx.guild_state.silent:
            ctx.guild_state.silent = 1
            await stop(ctx)
            ctx.guild_state.silent = 0
        else:
            await stop(ctx)

class QueueConrols(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
        self.page = 0
    
    def build_embed(self, guild):
        embed1 = discord.Embed(colour=0xdc8e10,title="**Currently Playing**", description=f"{guild.now_playing['title']}\nby {guild.now_playing['artist']}.")
        embed1.set_thumbnail(url=guild.now_playing["cover_art_url"])
        embeds = [embed1]
        description = ""
        rev_queue = list(reversed(guild.queue))
        for i in range((self.page*9), ((self.page+1)*9)):
            if i < len(rev_queue):
                description += f"**{i+1}:** {rev_queue[i]['title']} by {rev_queue[i]['artist']}.\n"
            else:
                break
        queue_embed = discord.Embed(colour=0xdc8e10,title="**Queue:** ", description=f"{description}")
        embeds.append(queue_embed)
        return embeds

    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page -= 1
        else:
            button.style=discord.ButtonStyle.grey
        guild = get_guild(interaction.guild.id)
        await interaction.response.edit_message(embeds=self.build_embed(guild), view=self)

    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = get_guild(interaction.guild.id)
        if self.page < ((len(guild.queue) - 1) // 9):
            self.page += 1 
        else:
            button.style=discord.ButtonStyle.grey
        await interaction.response.edit_message(embeds=self.build_embed(guild), view=self)