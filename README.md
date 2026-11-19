![Python](https://img.shields.io/badge/python-3.11+-blue)
![GitHub Stars](https://img.shields.io/github/stars/CringelBheem/navibot)


# NaviBot
NaviBot is an open-source Discord music bot built for Navidrome. Stream your self-hosted music library with full search, queue controls, synced lyrics support, autoplay, album playback, and an interactive Discord UI all in your discord voice channels.

## Features

- Stream music directly from Navidrome to discord
- Easy to use commands
- Queue management
- Full playback for songs and albums along with shuffle and random functionality
- Live synchronized lyrics
- Autoplay
- Silent mode to reduce spam
- Navidrome playlist controls

## Screenshots

### Command Suggestions

### Player Controls

### Queue Controls

### Live Lyrics

## Installation

### Requirements
- Python 3.11+
- Navidrome Server
- Discord Bot Token
### Setup
In order to host this bot for yourself, you first need to create a bot application using [Discord's Developer Portal](https://discord.com/developers/home).

You also need to host your music using Navidrome or have access to a Navidrome user account.

## Commands
Commands can be used with both / and ! prefixes. 
### Voice Connection Commands:
| Command  | Description                     |
| -------- | ------------------------------- |
| `/join`  | Join your current voice channel |
| `/leave` | Leave the voice channel         |

### Search Commands:
| Command                 | Description           |
| ----------------------- | --------------------- |
| `/search <query>`       | Search for tracks     |
| `/search_song <query>`  | Search for songs      |
| `/search_album <query>` | Search for albums     |
| `/search_artist <query>`| Search for artists    |
| `/play <query>`         | Play or queue a song  |
| `/play_album <query>`   | Queue an entire album |
| `/play_artist <query>`  | Play or queue a song  |
| `/play_random <count>`  | Queue random tracks   |
| `/play_random_album`    | Play a random album   |

### Playback Commands:
| Command     | Description                   |
| ----------- | ----------------------------- |
| `/playing`  | Show current track            |
| `/skip`     | Skip current track            |
| `/stop`     | Clear queue and stop playback |
| `/pause`    | Pause playback                |
| `/resume`   | Resume playback               |
| `/previous` | Play the previous track       |

### Queue Commands:
| Command                   | Description               |
| ------------------------- | ------------------------- |
| `/queue`                  | Show the queue            |
| `/shuffle`                | Shuffle the queue         |
| `/clear_queue`            | Clear the queue           |
| `/remove <position>`      | Remove a track            |
| `/move_up <position>`     | Move a track up           |
| `/move_down <position>`   | Move a track down         |
| `/move_top <position>`    | Move a track to the top   |
| `/move_bottom <position>` | Move a track to the bottom|

### Lyrics Commands:
| Command   | Description                 |
| --------- | --------------------------- |
| `/lyrics` | Display synchronized lyrics |

### Mode Commands:
| Command     | Description                       |
| ----------- | --------------------------------- |
| `/silent`   | Reduce message spam               |
| `/autoplay` | Automatically queue random tracks |

### Playlist Commands:
| Command                           | Description                    |
| --------------------------------- | ------------------------------ |
| `/create_playlist <name>`         | Create a playlist              |
| `/add_to_playlist <track>`        | Adds a track to a playlist     |
| `/search_playlist <name>`         | Searched tracks in a playlist  |
| `/play_playlist <name>`           | Plays all tracks in a playlist |
| `/remove_from_playlist <track>`   | Removes a track from a playlist|

# About this project


# Contributing

Pull requests are welcome.
- Fork the repository and clone it
- Create your feature branch
- Commit your changes
- Open a pull request
