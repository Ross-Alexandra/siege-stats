from siege_stats.bot.command import Command

class Clear(Command):

    @classmethod
    def command_string(self):
        return "=clear"

    async def clear_all(self, channel):
        async for message in channel.history(limit=100):
            if message.author.name == "AnalyticsBot":
                await message.delete()

    async def clear_errors(self, channel):
        async for message in channel.history(limit=100):
            if message.author.name == "AnalyticsBot" and message.content.startswith("Error:"):
                await message.delete()

    async def clear_most_recent(self, channel):
        async for message in channel.history(limit=100, oldest_first=False):
            if message.author.name == "AnalyticsBot":
                return await message.delete()

    async def execute(self, message, *args):
        try:
            if "all" in args:
                await self.clear_all(message.channel)

            elif "error" in args:
                await self.clear_errors(message.channel)

            else:
                await self.clear_most_recent(message.channel)

        except Exception as e:
            print(e)
            await message.channel.send(content="Error: An exception occurred while processing your request :(")
        finally:
            await message.delete()
