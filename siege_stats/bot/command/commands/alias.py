import traceback

from siege_stats.bot.command import Command

class Alias(Command):

    def _parse_args(self, args):
        if len(args) != 3:
            return {}

        else:
            return {
                "player_name": args[1].lower(),
                "alias": args[2].lower()
            }

    @staticmethod
    def command_string():
        return "=alias"

    async def execute(self, message, *args):
        try:
            arg_dict = self._parse_args(args)

            if not arg_dict:
                await message.channel.send(content=f"Error: Command usage is `=alias player_name player_alias`. Unable to process command {message.content}")
                return

            player_name = arg_dict["player_name"]
            player_alias = arg_dict["alias"]

            # Add forwards
            error_message = self._connection.add_alias(player_name, player_alias)
            if error_message:
                await message.channel.send(content=error_message)
                return

            # Add backwards, ensuring that an =playerstats will return the same
            # stats for both sides of the alias.
            error_message = self._connection.add_alias(player_alias, player_name)
            if error_message:
                await message.channel.send(content=error_message)
                return

        except Exception as e:
            print(f"Caught the following exception while processing alias command:")
            traceback.print_tb(e.__traceback__)
            print(e)
            await message.channel.send(content="Error: An exception occurred while processing your request :(")
        finally:
            await message.delete()

    def has_access(self, user_id, guild_id):
        """ Everyone can run alias command. """
        return True

    def can_execute(self, user_id, guild_id, *args):
        """ A player may only call this command if their guild has access to the aliased player. """
        if self._connection.is_user_admin(user_id):
            return True

        arg_dict = self._parse_args(args)
        if not arg_dict:
            return True # This will be caught and thrown out.

        players = [arg_dict["player_name"], arg_dict["alias"]]

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
