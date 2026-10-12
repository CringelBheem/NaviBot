
async def silent_response(guild, success):
    if guild.silent == 1:
        await success()

async def error_response(text, guild, respond, failure):
    if guild.silent == 0:
        await respond(text)
    elif guild.silent == 1:
        await failure()

async def join_check(ctx):
    if ctx.user_voice:
        channel = ctx.user_voice.channel
        voice = await channel.connect()
        if ctx.guild_state.silent == 0:
            await ctx.respond("Joined the voice channel.")
        return voice
    else:
        await error_response("You must be in a voice channel.", ctx.guild_state, ctx.respond, ctx.failure)
        return
