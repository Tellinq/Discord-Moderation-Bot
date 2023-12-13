from disnake.ext.commands import Cog, Bot, slash_command, option_enum
from disnake import ApplicationCommandInteraction, Member
from datetime import timedelta


class TimeoutCommand(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(ephemeral=True)
    async def timeout(self, interaction: ApplicationCommandInteraction): pass

    @timeout.sub_command()
    async def add(self, interaction: ApplicationCommandInteraction, member: Member, reason: str, duration: option_enum({"1 Day": 1, "7 Days": 7, "28 Days": 28})):
        try:
            await member.timeout(duration=timedelta(days=duration), reason=reason)
            await interaction.send(f"Timed out <@{member.id}> for {duration} day{"s" if duration > 1 else ""}.")
        except Exception as e:
            await interaction.response.send_message(e, ephemeral=True)

    @timeout.sub_command()
    async def remove(self, interaction: ApplicationCommandInteraction, member: Member, reason: str):
        try:
            await member.timeout(duration=None, reason=reason)
            await interaction.send(f"Removed timeout for <@{member.id}>.")
        except Exception as e:
            await interaction.response.send_message(e, ephemeral=True)
