import nextcord
from nextcord import Interaction
from nextcord.ext.commands import Cog, Bot

class AutoMod(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    @nextcord.slash_command()
    async def automod(self, interaction: Interaction): pass

    @automod.subcommand("add")
    async def add(interaction: Interaction): pass