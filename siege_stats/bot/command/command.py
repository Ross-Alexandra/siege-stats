from abc import abstractmethod, ABCMeta

from siege_stats.db.bot_db import BotDB

class Command(metaclass=ABCMeta):

    def __init__(self):
        self._connection = BotDB()

    def cleanup(self):
        self._connection.close()

    @staticmethod
    @abstractmethod
    def command_string(): 
        """ The command's string which will be included when a user
            attempt to run the command. """
        
        return

    @abstractmethod
    def has_access(self, user_id, guild_id):
        """ Checks whether a discord user or guild has permissions to run this command."""
        pass

    @abstractmethod
    def can_execute(self, user_id, guild_id, args):
        """ Checks whether a discord user or guild has permissions to access data requested in args"""
        pass

    @abstractmethod
    async def execute(self, message):
        """ The code to be run when a command is executed. """
        pass

    @staticmethod
    def _get_match_type(raw_string: str):
        if "scrim" in raw_string:
            return "scrim"
        elif "qual" in raw_string:
            return "qualifier"
        elif "league" in raw_string:
            return "league"
        else: 
            return None