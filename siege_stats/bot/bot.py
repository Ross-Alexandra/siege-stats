import siege_stats.bot.bot_settings as bot_settings
import discord
import io
import requests
import tempfile

from siege_stats.statistics_processing.stat_reader import StatReader
from siege_stats.db.bot_db import BotDB

class StatsBot(discord.Client):

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message: discord.Message):

        # If AnalyticsBot has not been mentioned, then ignore the message.
        if 'AnalyticsBot' not in [mention.name for mention in message.mentions]:
            print("Message did not mention AnalyticsBot.")
            return

        # If the message has no attachments, ignore it.
        if len(message.attachments) == 0 or not all([attachment.url.endswith('.csv') for attachment in message.attachments]):
            print("No attachments, or non-csv file included.")
            return
    
        # Define the match_type for use in the db.
        if "scrim" in message.channel.name:
            match_type = "scrim"
        elif "qual" in str(message.channel.name):
            match_type = "qualifier"
        elif "league" in str(message.channel.name):
            match_type = "league"
        else:
            print(f"csv uploaded in invalid text channel: {message.channel.name}. Ignoring.")
            return

        # Create a DB connection and parse out match statistics.
        db_conn = BotDB()
        match_statistics = self._get_match_stats([attachment.url for attachment in message.attachments])

        # Create a dictionary to hold the args for creating a match, and create the match object.
        kwargs = {
            "analyst_identifier": match_statistics.match_data["matchId"], 
            "map_str": match_statistics.match_data["mapString"],
            "match_type": match_type, 
            "rounds_won": match_statistics.match_data["roundsWon"], 
            "rounds_lost": match_statistics.match_data["roundsLost"], 
            "score_at_half": match_statistics.match_data["scoreAtHalf"], 
            "attackers_start": match_statistics.match_data["start_attack"]
        }
        match_id, match_created = db_conn.add_match(**kwargs)

        # If that match already exists, then ignore this row.
        if not match_created:
            print(f"Match already exists in database. Ignoring.")
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
    client = StatsBot()
    client.run(bot_settings.bot_token)
