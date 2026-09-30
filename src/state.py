class GuildState:
    def __init__(self):
        self.queue = []
        self.silent = 0
        self.autoplay = 0
        self.now_playing = {
            "title": "",
            "artist": "",
            "track_id": ""
        }
        self.history = []
        
guilds = {}

def get_guild(guild_id) -> dict:
    if guild_id not in guilds:
        guilds[guild_id] = GuildState()
    return guilds[guild_id]

class CommandContext:
    def __init__(self, guild_state, voice, respond, success, failure, user_voice):
        self.guild_state = guild_state
        self.voice = voice
        self.respond = respond
        self.success = success
        self.failure = failure
        self.user_voice = user_voice