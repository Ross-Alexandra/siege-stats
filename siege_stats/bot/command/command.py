from abc import abstractmethod, abstractclassmethod

class Command:

    @abstractclassmethod
    def command_string(self): 
        """ The command's string which will be included when a user
            attempt to run the command. """
        
        return

    @abstractmethod
    async def execute(self, message):
        """ The code to be run when a command is executed. """

        return

    @staticmethod
    def _get_match_type_from_channel(message):
        if "scrim" in message.channel.name:
            return "scrim"
        elif "qual" in str(message.channel.name):
            return "qualifier"
        elif "league" in str(message.channel.name):
            return "league"
        else: 
            return None