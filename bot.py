import disnake
from disnake.ext import commands
import sqlite3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_IDS = [int(guild_id.strip()) for guild_id in os.getenv('TEST_GUILD_IDS').split(',')]
intents = disnake.Intents.all()
bot = commands.Bot(intents=intents, command_prefix=None)


# SQLite setup
conn = sqlite3.connect('bot_data.db')
cursor = conn.cursor()

# Database structure setup
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cooldowns (
        user_id INTEGER PRIMARY KEY,
        last_notified TIMESTAMP
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS watched_titles (
        title TEXT PRIMARY KEY
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS opted_out_users (
        user_id INTEGER PRIMARY KEY
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS lfg_channel (
        guild_id INTEGER PRIMARY KEY,
        channel_id INTEGER
    )
''')
conn.commit()

# Config commands setup
class LFGCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="lfgchannel", description="Set the LFG notification channel", guild_ids=[GUILD_IDS])
    @commands.has_permissions(manage_guild=True)
    async def lfg_channel(self, ctx, channel: disnake.TextChannel):
        cursor.execute("INSERT OR REPLACE INTO lfg_channel (guild_id, channel_id) VALUES (?, ?)",
                       (ctx.guild.id, channel.id))
        conn.commit()
        await ctx.send(f"Set the LFG notification channel to {channel.mention}!", ephemeral=True)

    @commands.slash_command(name="watchtitle", description="Add a title to be watched for LFG notifications", guild_ids=[GUILD_IDS])
    @commands.has_permissions(manage_guild=True)
    async def watch_title(self, ctx, title: str):
        cursor.execute("INSERT INTO watched_titles (title) VALUES (?)", (title,))
        conn.commit()
        await ctx.send(f"Added '{title}' to watched titles.", ephemeral=True)
   
    @commands.slash_command(name="unwatchtitle", description="Remove a title from being watched", guild_ids=[GUILD_IDS])
    @commands.has_permissions(manage_guild=True)
    async def unwatch_title(self, ctx, title: str):
        cursor.execute("DELETE FROM watched_titles WHERE title=?", (title,))
        conn.commit()
        await ctx.send(f"Removed '{title}' from watched titles.", ephemeral=True)

    @commands.slash_command(name="optout", description="Opt-out of LFG notifications", guild_ids=[GUILD_IDS])
    async def opt_out(self, ctx):
        cursor.execute("INSERT INTO opted_out_users (user_id) VALUES (?)", (ctx.author.id,))
        cursor.execute("DELETE FROM cooldowns WHERE user_id=?", (ctx.author.id,))
        conn.commit()
        await ctx.send("You've opted out of LFG notifications.", ephemeral=True)

bot.add_cog(LFGCommands(bot))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Activity monitor setup
@bot.event
async def on_presence_update(before, after):
    cursor.execute("SELECT user_id FROM opted_out_users WHERE user_id=?", (after.id,))
    if cursor.fetchone():
        return

    if after.activities:
        cursor.execute("SELECT title FROM watched_titles")
        watched_titles = {row[0] for row in cursor.fetchall()}

        for activity in after.activities:

            if activity.name in watched_titles:
                cursor.execute("SELECT last_notified FROM cooldowns WHERE user_id=?", (after.id,))
                result = cursor.fetchone()
                if result:
                    last_notified = datetime.fromisoformat(result[0])
                    if datetime.utcnow() - last_notified < timedelta(minutes=10):
                        return
                    
                cursor.execute("SELECT channel_id FROM lfg_channel WHERE guild_id=?", (after.guild.id,))
                lfg_channel_id = cursor.fetchone()
                if lfg_channel_id:
                    lfg_channel = after.guild.get_channel(lfg_channel_id[0])
                    if lfg_channel:
                        await lfg_channel.send(f"{after.user.display_name} has started playing {activity.name}!")
                        cursor.execute("INSERT OR REPLACE INTO cooldowns (user_id, last_notified) VALUES (?, ?)",
                                       (after.id, datetime.utcnow().isoformat()))
                        conn.commit()

bot.run(TOKEN)
