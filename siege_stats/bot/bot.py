import siege_stats.bot.bot_settings as bot_settings
import discord
import io
import re
import requests
import tempfile

from siege_stats.statistics_processing.stat_reader import StatReader, Stats
from siege_stats.db.bot_db import BotDB

class StatsBot(discord.Client):

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message: discord.Message):
        # If AnalyticsBot has not been mentioned, then ignore the message.
        if 'AnalyticsBot' not in [mention.name for mention in message.mentions]:
            return

        # Strip any mentions out of the content of the message.
        message_content = re.sub(r'<.+?>', '', message.content).strip()

        if len(message.attachments) != 0:
            await self.process_file(message)

        if message_content.lower().startswith("=playerstats"):
            for player in message_content.split(" ")[1:]:
                await self.post_player_stats(player, message)

    def _get_match_type_from_channel(self, message):
            if "scrim" in message.channel.name:
                return "scrim"
            elif "qual" in str(message.channel.name):
                return "qualifier"
            elif "league" in str(message.channel.name):
                return "league"
            else: 
                return None

    async def post_player_stats(self, player_name, message):
        try:
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

    async def process_file(self, message: discord.Message):

        try:
            # If the message has no attachments, ignore it.
            if len(message.attachments) == 0 or not all([attachment.url.endswith('.csv') for attachment in message.attachments]):
                print("No attachments, or non-csv file included.")

                await message.channel.send(content="Error: What do you want from me? There's no file attached...")
                return
        
            match_type = self._get_match_type_from_channel(message)
            if match_type is None:
                print(f"csv uploaded in invalid text channel: {message.channel.name}. Ignoring.")
                await message.channel.send(content="Error: I can't figure out what type of match this is, please post in a channel with scrim, qual, or league in it's name.")
                return

            # Create a DB connection and parse out match statistics.
            db_conn = BotDB()
            match_statistics = self._get_match_stats([attachment.url for attachment in message.attachments])

            team_id, _ = db_conn.add_team(match_statistics.player_stats.keys())

            # Create a dictionary to hold the args for creating a match, and create the match object.
            kwargs = {
                "analyst_identifier": match_statistics.match_data["matchId"], 
                "map_str": match_statistics.match_data["mapString"],
                "match_type": match_type, 
                "rounds_won": match_statistics.match_data["roundsWon"], 
                "rounds_lost": match_statistics.match_data["roundsLost"], 
                "score_at_half": match_statistics.match_data["scoreAtHalf"], 
                "attackers_start": match_statistics.match_data["start_attack"],
                "team_id": team_id,
            }
            match_id, match_created = db_conn.add_match(**kwargs)

            # If that match already exists, then ignore this row.
            if not match_created:
                print(f"Match already exists in database. Ignoring.")

                await message.channel.send(content="Error: I already have data for this match :/")
                return


            for player_name, stat_object in match_statistics.player_stats.items():
                # Create a dictionary to hold the args for creating a stats object and create the stats object.
                kwargs = {
                    "player": player_name,
                    "match_id": match_id, 
                    "map_string": match_statistics.match_data["mapString"],
                    "rating": stat_object.get_rating(),
                    "attack_rating": stat_object.get_attack_rating(),
                    "defence_rating": stat_object.get_defence_rating(),
                    "kill_differential": stat_object.get_kill_differential(),
                    "entry_differential": stat_object.get_entry_differential(),
                    "trade_differential": stat_object.get_trade_differential(),
                    "kost": stat_object.get_kost(),
                    "kills_per_round": stat_object.get_kills_per_round(),
                    "survival_percentage": stat_object.get_survival_percent(),
                    "headshot_percentage": stat_object.get_headshot_percent(),
                    "multi_kill_rounds": stat_object.get_multi_kill_rounds(),
                    "deaths": stat_object.get_deaths(),
                    "kills": stat_object.get_kills(),
                    "defuser_planted": stat_object.get_defuser_planted(),
                    "defuser_disabled": stat_object.get_defuser_disabled(),
                    "team_kills": stat_object.get_team_kills()
                }
                db_conn.add_statistic(**kwargs)

        except Exception as e:
            print(e)
            await message.channel.send(content="Error: An exception has occurred while processing the request :(")
        finally:
            await message.delete()
            try:
                db_conn.close()
            except Exception:
                pass

    @staticmethod
    def _temp_download_file(url):
        """ Takes in a url and returns a file object of the temp file."""

        # Get the contents from the url
        r = requests.get(url, stream=True)
        temp = io.StringIO(r.content.decode())

        return temp

    def _get_match_stats(self, urls):
        temp_files = [self._temp_download_file(url) for url in urls]

        sr = StatReader()
        for temp in temp_files:
            sr.collect_match_overview(temp)
            sr.collect_match_performance(temp)
            temp.close()

        return sr

if __name__ == "__main__":
    from siege_stats.db.db_settings import db_pass

    client = StatsBot()
    client.run(bot_settings.bot_token)