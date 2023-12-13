from disnake.ext.commands import Cog, Bot, slash_command
from disnake import ApplicationCommandInteraction

class AutoModCommand(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    @slash_command()
    async def automod(self, interaction: ApplicationCommandInteraction): pass

    @automod.sub_command("add")
    async def add(interaction: ApplicationCommandInteraction): pass