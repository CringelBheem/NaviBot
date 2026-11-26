import  os
import aiohttp
import hashlib
import random
import string
from dotenv import load_dotenv

load_dotenv()



class NavidromeClient:
    def __init__(self):
        self.session = None
        self.password = os.getenv("NAVIDROME_PASSWORD")
        self.url = os.getenv("NAVIDROME_URL")

    async def start(self):
        self.session = aiohttp.ClientSession()

    def generate_token(self):
        
        salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        token = hashlib.md5((self.password + salt).encode('utf-8')).hexdigest()
        return token, salt

    def auth_params(self):
        token, salt = self.generate_token()

        return {
            "u": "NaviBot",
            "t": token,
            "s": salt,
            "v": "1.16.1",
            "c": "Navi Bot",
            "f": "json",
        }

    async def search_navidrome(self, query, s_type):
        params = {
            **self.auth_params(),
            "query": query,
        }
        
        url = self.url+f"/rest/{s_type}"

        async with self.session.get(url, params=params) as r:
            r.raise_for_status()
            data = await r.json()

        try:
            return data["subsonic-response"]["searchResult2"]
        except KeyError:
            return {
                "artist": [],
                "album": [],
                "song": []
            }

    async def search_album(self, query):
        url = self.url+f"/rest/getAlbum"
        
        results = await self.search_navidrome(query, "search2")
        albums = results.get("album", [])
        if not albums:
            return []
        album_id = albums[0]["id"]


        params = {
            **self.auth_params(),
            "id": album_id
            }
        

        async with self.session.get(url, params=params) as r:
            r.raise_for_status()
            data = await r.json()
            
        try:
            return data["subsonic-response"]["album"]["song"]
        except KeyError:
            return []
    
    async def search_random(self, size):
        url = self.url+f"/rest/getRandomSongs"
    
        params = {
            **self.auth_params(),
            "size": size if size else 1
            }
        
        async with self.session.get(url, params=params) as r:
            r.raise_for_status()
            data = await r.json()

        try:
            return data["subsonic-response"]["randomSongs"]["song"]
        except KeyError:
            return []
        
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
