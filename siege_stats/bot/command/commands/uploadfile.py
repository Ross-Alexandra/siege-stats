import io
import requests
import traceback

from siege_stats.statistics_processing.stat_reader import StatReader
from siege_stats.bot.command import Command
from siege_stats.db.bot_db import BotDB

class UploadFile(Command):

    @staticmethod
    def command_string():
        return "=uploadfile"

    async def execute(self, message, *args):
        try:
            # If the message has no attachments, ignore it.
            if len(message.attachments) == 0 or not all([attachment.url.endswith('.csv') for attachment in message.attachments]):
                print("No attachments, or non-csv file included.")

                await message.channel.send(content="Error: What do you want from me? There's no file attached...")
                return
        
            if len(args) > 1:
                raw_match_type = self._get_match_type(args[1])
                match_type = raw_match_type if raw_match_type is not None else self._get_match_type(message.channel.name) 
            else:
                match_type = self._get_match_type(message.channel.name)

            if match_type is None:
                print(f"csv uploaded with no indication of tag. Ignoring")
                await message.channel.send(content="Error: I can't figure out what type of match this is, please run one of '=uploadfile scrim', '=uploadfile qual', or '=uploadfile league'.")
                return

            # Create a DB connection and parse out match statistics.
            self._connection = BotDB()
            match_statistics = self._get_match_stats([attachment.url for attachment in message.attachments])

            team_id = self._get_or_create_guild_team(message.guild, match_statistics.player_stats.keys())

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
            match_id, match_created = self._connection.add_match(**kwargs)

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
                self._connection.add_statistic(**kwargs)

        except Exception as e:
            print("An error occurred while processing the file")
            traceback.print_tb(e.__traceback__)
            print(e)
            await message.channel.send(content="Error: An exception has occurred while processing the request :(")
        finally:
            await message.delete()
    
    def has_access(self, player_id, guild_id):
        """ Everyone has access to uploading files. """
        return True
    
    def can_execute(self, player_id, guild_id, *args):
        """ Everyone has the ability run with all arguments. """
        return True

    def _get_match_stats(self, urls):
        temp_files = [self._temp_download_file(url) for url in urls]

        sr = StatReader()
        for temp in temp_files:
            sr.collect_match_overview(temp)
            sr.collect_match_performance(temp)
            temp.close()

        return sr

    def _get_or_create_guild_team(self, guild, players):

        team_id = self._connection.get_team_id_by_name(guild.name)

        if team_id is None:
            old_guild_name = self._connection.get_guild_name(guild.id)
            if old_guild_name is None:
                self._connection.add_guild(guild.id, guild.name)
                old_guild_name = guild.name

            # No team has been registerd for this guild
            if old_guild_name == guild.name:
                team_id, _ = self._connection.add_team(players)

                self._connection.set_team_name(team_id, guild.name)
                self._connection.give_guild_team_permissions(guild.id, team_id)

            # The guild has changed names
            else:
                team_id = self._connection.get_team_id_by_name(old_guild_name)

                self._connection.update_guild_name(guild.id, guild.name)
                self._connection.set_team_name(team_id, guild.name)

        # Attempt to insert the new players into a team.
        # This allows teams to have more than 5 players (since
        # this is in a guild, we assume these are subs or whatever.)
        for player in players:
            self._connection.add_player_to_team(team_id, player)

        return team_id

    @staticmethod
    def _temp_download_file(url):
        """ Takes in a url and returns a file object of the temp file."""

        # Get the contents from the url
        r = requests.get(url, stream=True)
        temp = io.StringIO(r.content.decode())

        return temp
