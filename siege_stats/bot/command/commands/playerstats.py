from siege_stats.bot.command.command import Command
import inspect
from siege_stats.db.bot_db import BotDB
from siege_stats.statistics_processing.stat_reader import Stats


class PlayerStats(Command):

    @classmethod
    def command_string(self):
        return "=playerstats"

    async def execute(self, message, *args):
        try:
            
            # Iterate through the arguments and process each player.
            # First argument is the =playerstats command so ignore it.
            for player_name in args[1:]:

                db_conn = BotDB()

                match_type = self._get_match_type_from_channel(message)
                raw_stats = db_conn.get_player_stats(player_name, match_type)
                player_stat = Stats()

                for stat in raw_stats:
                    # Break the stat down into it's parts, the 
                    # db requested the data in the correct order for this.
                    player_stat += Stats(*stat)

                response = f"{player_name} {match_type if match_type is not None else 'aggregate'} {player_stat}"
                await message.channel.send(content=response)

        except Exception as e:
            print(e)
            await message.channel.send(content="Error: An exception occurred while processing your request :(")
        finally:
            await message.delete()
            db_conn.close()
