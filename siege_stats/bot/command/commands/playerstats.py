from siege_stats.bot.command import Command
from siege_stats.db.bot_db import BotDB
from siege_stats.statistics_processing.stat_reader import Stats


class PlayerStats(Command):

    def _parse_args(self, *args):

        match_type = self._get_match_type(args[1])

        return {
            "command": args[0],
            "match_type": match_type,
            "players": [arg.lower() for arg in args[2:]] if match_type else [arg.lower() for arg in args[1:]]
        }

    def execute_permission_error_message(self, user, guild, arguments):
        response = ""
        
        players = self._parse_args(*arguments)["players"]
        for player_name in players:
            response += f"No data for {player_name}\n"
        
        return response

    @staticmethod
    def command_string():
        return "=playerstats"

    async def execute(self, message, *args):
        try:
            db_conn = BotDB()
            parse_dict = self._parse_args(*args)
            match_type = parse_dict["match_type"] if parse_dict["match_type"] else self._get_match_type(str(message.channel.name))

            # Iterate through the arguments and process each player.
            # First argument is the =playerstats command so ignore it.
            for player_name in parse_dict["players"]:
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

    def has_access(self, user_id, guild_id):
        # Anyone may call this command.
        return True

    def can_execute(self, user_id, guild_id, *args):
        if self._connection.is_user_admin(user_id):
            return True

        players = self._parse_args(*args)["players"]
        team_ids = {player: self._connection.get_all_teams_for_player(player) for player in players}

        # Check if the user has team permissions for *any* of the teams which 
        # a player is on. If the user has none, then we still don't have permission
        # for that player.
        players = [player for player in players if not any([self._connection.user_has_team_permissions(user_id, team_id) for team_id in team_ids[player]])]
        if players == []:
            return True

        # Check if the guild has team permissions for *any* of the teams which 
        # a player is on. If the guild has none, then we still don't have permission
        # for that player.
        players = [player for player in players if not any([self._connection.guild_has_team_permissions(guild_id, team_id) for team_id in team_ids[player]])]
        if players == []:
            return True

        # Check if the user has player permissions for the player. If the user
        # has none, then we still don't have permission for that player.
        players = [player for player in players if not self._connection.user_has_player_permissions(user_id, player)]
        if players == []:
            return True

        # Check if the guild has player permissions for the player. If the guild
        # has none, then we still don't have permission for that player.
        players = [player for player in players if not self._connection.guild_has_player_permissions(guild_id, player)]

        # At this point we've checked the combonation of player and guild permissions.
        # if any players still exist in [players] then there are missing permissions.
        return players == []
