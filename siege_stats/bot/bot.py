import siege_stats.bot.bot_settings as bot_settings
import discord
import re

from siege_stats.bot.command.command_parser import CommandParser

class StatsBot(discord.Client):

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

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