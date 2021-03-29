import siege_stats.bot.bot_settings as bot_settings
import discord
import re

from siege_stats.bot.command.command_parser import CommandParser
from siege_stats.db.bot_db import BotDB

class StatsBot(discord.Client):

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
        print("I am in the following servers: ")
        for guild in self.guilds:
            print(f"{guild.name}: {guild.id}")

    async def on_guild_join(self, guild):
        try:
            dbcon = BotDB()
            dbcon.add_guild(guild.id, guild.name)
            print(f"Joined guild: {guild.id} with {guild.name}")
        except Exception as e:
            print(f"Failed to add guild to database due to {e}")
        finally:
            dbcon.close()

    async def on_message(self, message: discord.Message):
        # If AnalyticsBot has not been mentioned, then ignore the message.
        if 'AnalyticsBot' not in [mention.name for mention in message.mentions]:
            return

        cp = CommandParser(message)
        await cp.run()

if __name__ == "__main__":
    from siege_stats.db.db_settings import db_pass

    client = StatsBot()
    client.run(bot_settings.bot_token)
