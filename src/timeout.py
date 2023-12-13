import nextcord
from nextcord import Interaction, Member
from datetime import timedelta
from nextcord.ext.commands import Cog, Bot


class Timeout(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command()
    async def timeout(self, interaction: Interaction): pass

    @timeout.subcommand("days")
    async def days(self, interaction: Interaction, member: Member, reason: str, days: int):
        try:
            if (days in range(1, 30)):
                await member.timeout(timeout=timedelta(days=days), reason=reason)
                await interaction.send(f"{member.global_name} has been timed out for {days} day(s).")
            else:
                await interaction.send("You can timeout a member for 1 ~ 30 days.")
        except Exception as exception:
            await interaction.send(exception)

    @timeout.subcommand("weeks")
    async def weeks(self, interaction: Interaction, member: Member, reason: str, weeks: int):
        try:
            if (weeks in range(1, 5)):
                await member.timeout(timeout=timedelta(weeks=weeks), reason=reason)
                await interaction.send(f"{member.global_name} has been timed out for {weeks} week(s).")
            else:
                await interaction.send("You can timeout a member for 1 ~ 4 weeks.")
        except Exception as exception:
            await interaction.send(exception)

    @timeout.subcommand("month")
    async def month(self, interaction: Interaction, member: Member, reason: str):
        try:
            await member.timeout(timeout=timedelta(weeks=4), reason=reason)
            await interaction.send(f"{member.global_name} has been timed out for a month.")
        except Exception as exception:
            await interaction.send(exception)

    @timeout.subcommand("remove")
    async def remove(self, interaction: Interaction, member: Member, reason: str):
        try:
            await member.timeout(None, reason=reason)
            await interaction.send(f"Removed timeout for {member.global_name}.")
        except Exception as exception:
            await interaction.send(exception)
