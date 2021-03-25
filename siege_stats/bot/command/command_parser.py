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
        author = self.message.author
        guild = self.message.guild

        for subclass in Command.__subclasses__():
            if message_content.lower().startswith(subclass.command_string()):
                command = subclass()
 
                if command.has_access(author.id, guild.id):
                    command_arguments = message_content.split(" ")

                    if command.can_execute(author.id, guild.id, *command_arguments):
                        command_response = await command.execute(self.message, *command_arguments)
                    else:
                        return await self.message.channel.send(content=f"Error: Neither {author.name} ({author.id}) nor {guild.name} ({guild.id}) have permissions to run {command_arguments[0]} with {command_arguments[1:]}.")

                    command.cleanup()
                else:
                    return await self.message.channel.send(content=f"Error: Neither {author.name} ({author.id}) nor {guild.name} ({guild.id}) have permission for this command.")

                return command_response

        print(f"Unknown command: {message_content.lower()}")
