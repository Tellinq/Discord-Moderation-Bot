import disnake
from disnake.ext import commands, plugins

import datetime
import dateparser

plugin = plugins.Plugin()


def parse_punishment_duration(duration: str) -> datetime.datetime:
    settings = {
        "TIMEZONE": "UTC",
        "RETURN_AS_TIMEZONE_AWARE": True,
        "PREFER_DATES_FROM": "future",
    }
    date = dateparser.parse(duration, settings=settings) # type: ignore
    if date is None:
        raise commands.BadArgument(f"Invalid duration: '{duration}'.")
    return date


def format_timeout_duration(member: disnake.Member) -> str:
    assert member.current_timeout is not None
    return disnake.utils.format_dt(member.current_timeout, 'R')


def make_timeout_message(target: disnake.Member, reason: str) -> str:
    return f"Timed out {target.mention} for **'{reason}'**.\nExpiry: {format_timeout_duration(target)}."
    

class TimeoutPrompt(disnake.ui.View):
    def __init__(self, author: disnake.Member, target: disnake.Member, timeout_duration: datetime.datetime, reason: str):
        super().__init__(timeout=45.0)
        self.author = author
        self.target = target
        self.timeout_duration = timeout_duration
        self.reason = reason

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, disnake.ui.Button):
                self.remove_item(child)

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        if self.author != interaction.author:
            await interaction.send("You can't do that.", ephemeral=True)
            return False
        return True

    @disnake.ui.button(label="Overwrite", style=disnake.ButtonStyle.green) 
    async def overwrite(self, button: disnake.ui.Button, inter: disnake.MessageInteraction): # type: ignore
        await self.target.timeout(until=self.timeout_duration, reason=self.reason)
        await inter.response.edit_message(make_timeout_message(self.target, self.reason), components=None)
        self.stop()

    @disnake.ui.button(label="Increase", style=disnake.ButtonStyle.primary) 
    async def increase(self, button: disnake.ui.Button, inter: disnake.MessageInteraction): # type: ignore
        await inter.response.edit_message("todo", components=None)
        self.stop()

    @disnake.ui.button(label="Cancel", style=disnake.ButtonStyle.danger) 
    async def cancel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction): # type: ignore
        await inter.response.edit_message("Canceled.", components=None)
        self.stop()


@plugin.slash_command()
@commands.bot_has_permissions(moderate_members=True)
@commands.has_permissions(moderate_members=True)
async def timeout(inter: disnake.GuildCommandInteraction):
    """Timeout commands"""
    pass


@timeout.sub_command()
async def add(inter: disnake.GuildCommandInteraction, target: disnake.Member, reason: str, duration: str):
    """
    Timeout a member

    Parameters
    ----------
    target: The member to timeout
    reason: The reason for timeout
    duration: Duration of the timeout
    """

    timeout_duration = parse_punishment_duration(duration)

    if target.current_timeout is None:
        await target.timeout(until=timeout_duration, reason=reason)
        await inter.send(make_timeout_message(target, reason))
        return
    
    await inter.response.defer()

    view = TimeoutPrompt(inter.author, target, timeout_duration, reason)

    await inter.send(f"That user is already timed out. Expiry: {format_timeout_duration(target)}, do you want to overwrite it?", view=view)
    await view.wait()


@timeout.sub_command()
async def remove(inter: disnake.GuildCommandInteraction, target: disnake.Member, reason: str):
    """
    Remove timeout from a user

    Parameters
    ----------
    target: The member to remove timeout from
    reason: The reason for the timeout being removed
    """

    if target.current_timeout is None:
        raise commands.BadArgument("That user is not timed out.")
    
    await target.timeout(until=None, reason=reason)
    await inter.send(f"Removed timeout for {target.mention}. \nReason: '{reason}'")


@timeout.sub_command()
async def check(inter: disnake.GuildCommandInteraction, target: disnake.Member):
    """
    See when a member's timeout expires

    Parameters
    ----------
    target: The member to remove timeout from
    """

    if target.current_timeout is None:
        raise commands.BadArgument("That user is not timed out.")
    
    await inter.send(f"{target.mention}'s timeout expires {format_timeout_duration(target)}")


setup, teardown = plugin.create_extension_handlers()