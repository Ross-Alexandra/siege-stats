import io
import re
import requests

from siege_stats.statistics_processing.stat_reader import StatReader, Stats

from siege_stats.bot.command import Command

class CommandParser:

    def __init__(self, message):
        self.message = message

    async def run(self):
        # Strip any mentions out of the content of the message.
        message_content = re.sub(r'<.+?>', '', self.message.content).strip()

        for subclass in Command.__subclasses__():
            if message_content.lower().startswith(subclass.command_string()):
                return await subclass().execute(self.message, *message_content.split(" "))

        print(f"Unknown command: {message_content.lower()}")
