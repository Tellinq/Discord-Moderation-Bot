from disnake.ext.commands import Cog, Bot, slash_command
from disnake import CmdInter


class AutoMod(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        
        
    @slash_command()
    async def automod(self, inter: CmdInter):
        pass


    @automod.sub_command()
    async def placeholder(inter: CmdInter):
        """Placeholder."""
        pass
    


def setup(bot: Bot):
    print("Loaded Automod Cog")
    bot.add_cog(AutoMod(bot))