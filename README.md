![Python](https://img.shields.io/badge/python-3.11+-blue)
![GitHub Stars](https://img.shields.io/github/stars/CringelBheem/navibot)


# NaviBot
NaviBot is an open-source music player bot for discord that streams your navidrome music collection.


## Features

- Stream music directly from Navidrome to discord
- Easy to use commands
- Queue management
- Full playback for songs and albums along with shuffle and random functionality
- Live synchronized lyrics
- Autoplay
- Silent mode to reduce spam

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
| Command               | Description           |
| --------------------- | --------------------- |
| `/search <query>`     | Search for tracks     |
| `/play <query>`       | Play or queue a song  |
| `/playalbum <query>`  | Queue an entire album |
| `/playrandom <count>` | Queue random tracks   |
| `/playrandomalbum`    | Play a random album   |

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
| Command              | Description       |
| -------------------- | ----------------- |
| `/queue`             | Show the queue    |
| `/shufflequeue`      | Shuffle the queue |
| `/clearqueue`        | Clear the queue   |
| `/remove <position>` | Remove a track    |

### Lyrics Commands:
| Command   | Description                 |
| --------- | --------------------------- |
| `/lyrics` | Display synchronized lyrics |

### Mode Commands:
| Command     | Description                       |
| ----------- | --------------------------------- |
| `/silent`   | Reduce message spam               |
| `/autoplay` | Automatically queue random tracks |

# About this project


# Contributing

Pull requests are welcome.
- Fork the repository and clone it
- Create your feature branch
- Commit your changes
- Open a pull request
