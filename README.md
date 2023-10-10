# LFGScout
![](https://i.imgur.com/aEgp7Qo.png)
![GitHub top language](https://img.shields.io/github/languages/top/djstompzone/lfgscout)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/DJStompZone/LFGScout)
[![CodeQL](https://github.com/DJStompZone/LFGScout/actions/workflows/codeql.yml/badge.svg)](https://github.com/DJStompZone/LFGScout/actions/workflows/codeql.yml)
<a href="https://discord.gg/stompzone"><img src="https://img.shields.io/discord/599808270655291403?color=blue&label=Discord&logo=discord&logoColor=blue"></a>

## About
LFGScout is a Discord bot designed to monitor and notify when members of a guild start playing a specific game. The bot uses the Disnake (a Python wrapper for the Discord API) and SQLite3 for database management.

![Static Badge](https://img.shields.io/badge/OS-Windows-White?style=flat&logo=Windows&logoColor=White&label=%20&labelColor=black)
![Static Badge](https://img.shields.io/badge/OS-Linux-White?style=flat&logo=Linux&logoColor=White&label=%20&labelColor=black)
![Static Badge](https://img.shields.io/badge/OS-Mac%20OS-White?style=flat&logo=Apple&logoColor=White&label=%20&labelColor=black)

## Features
- Monitor members' game activities in real-time.
- Notify a specified channel when someone starts playing a watched title.
- Admin commands to configure the notification channel and watched titles.
- Users can opt-out of notifications.
- Cooldown feature to prevent spamming notifications.

## Setup & Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/DJStompZone/LFGScout
    cd LFGScout
    ```

2. Set up a virtual environment (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows use: venv\Scripts\activate
    ```

3. Install the required dependencies
    ```bash
    pip install -r requirements.txt
    ```

4. Configure your environment
   
    Copy the example.env file to .env and fill out the DISCORD_TOKEN and TEST_GUILD_IDS with appropriate values.

6. Run the bot
    ```bash
    python bot.py
    ```

## Commands

### Admin Commands:

- `/lfgchannel <#channel>`: Set the channel where notifications will be sent.

- `/watchtitle <title>`: Add a game title to the watch list.

- `/unwatchtitle <title>`: Remove a game title from the watch list.

### User Commands:

- `/optout`: Allows a user to opt out of LFG notifications.

## Contribution
Feel free to [fork](https://github.com/DJStompZone/LFGScout/fork) the project, make some improvements, and submit a [pull request](https://github.com/DJStompZone/LFGScout/pulls).

## Issues & Bug Reports
Found a bug? Just create an [issue](https://github.com/DJStompZone/LFGScout/issues) and describe the problem.
You can also join the [StompZone Discord](https://discord.gg/stompzone) to see the bot in action or join our growing community.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

### Disnake
A Python wrapper for the Discord API.<br>
[Docs](https://docs.disnake.dev/en/stable/) | [GitHub](https://github.com/DisnakeDev/disnake) | [Discord](https://discord.gg/disnake)

### SQLite
A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.<br>
[Homepage](https://www.sqlite.org/index.html)
