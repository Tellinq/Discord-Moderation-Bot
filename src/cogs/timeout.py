from disnake.ext.commands import Cog, Bot, slash_command
from disnake import CmdInter


class Timeout(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    @slash_command()
    async def timeout(self, inter: CmdInter): 
        """Timeout a member."""
        pass
    

def setup(bot: Bot):
    print("Loaded Timeout Cog")
    bot.add_cog(Timeout(bot))