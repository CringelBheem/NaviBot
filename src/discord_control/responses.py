
async def silent_response(guild, success):
    if guild.silent == 1:
        await success()
        #await message.delete(delay=2)

async def error_response(text, guild, respond, failure):
    if guild.silent == 0:
        await respond(text)
    elif guild.silent == 1:
        await failure()
        #await message.delete(delay=2)

async def join_check(ctx):
    if ctx.user_voice:
        channel = ctx.user_voice.channel
        await channel.connect()
        if ctx.guild_state.silent == 0:
            await ctx.respond("Joined the voice channel.")
        voice = ctx.voice
        return voice
    else:
        await error_response("You must be in a voice channel.", ctx.guild_state, ctx.respond, ctx.failure)
        return
