import  os
import aiohttp
import hashlib
import random
import string
from dotenv import load_dotenv

load_dotenv()



class NavidromeClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        self.token = hashlib.md5((os.getenv("NAVIDROME_PASSWORD") + self.salt).encode('utf-8')).hexdigest()

    async def search_navidrome():
        pass

    async def search_album():
        pass

    async def search_random():
        pass

    async def build_stream_url():
        pass

    async def get_image(coverArt):
        pass

    async def get_lyrics(track_id):
        pass

    async def create_playlist(name):
        pass

    async def add_to_playlist(id, song_id):
        pass

    async def get_playlist_id(name):
        pass

    async def get_playlist(id):
        pass

    async def get_playlists(name):
        pass

    async def remove_from_playlist(id, index):
        pass

    async def search_artist(query):
        pass
