import disnake
from disnake.ext import plugins, commands

import datetime
import dateparser
import asyncio


plugin = plugins.Plugin()


TIMEOUT_PROMPT_WAIT_SECS = 45

def parse_punishment_duration(duration: str) -> datetime.datetime:
    settings = {
        "TIMEZONE": "UTC",
        "RETURN_AS_TIMEZONE_AWARE": True,
        "PREFER_DATES_FROM": "future",
    }
    date = dateparser.parse(duration, settings=settings) # type: ignore
    if date is None:
        raise commands.BadArgument(f"Invalid duration: '{duration}'.") # message can be tweaked
    return date


def hierarchy_check(inter: disnake.GuildCommandInteraction, target: disnake.User | disnake.Member):
    if inter.guild.owner == target:
        raise commands.BadArgument("I cannot perform that action on the server owner.")
    
    if inter.guild.me == target:
        raise commands.BadArgument("I cannot perform that action on myself.")
    
    if isinstance(target, disnake.Member):
        if inter.author.top_role <= target.top_role:
            raise commands.BadArgument("You cannot perform that action on a user higher up or on the same level in the role hierarchy as you.")
        if inter.guild.me.top_role <= target.top_role:
            raise commands.BadArgument("I cannot perform that action on a user higher up or on the same level in the role hierarchy as me.")


def format_timeout_duration(member: disnake.Member) -> str:
    assert member.current_timeout is not None
    return disnake.utils.format_dt(member.current_timeout, 'R')


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

    hierarchy_check(inter, target)
    timeout_duration = parse_punishment_duration(duration)

    make_timeout_message = lambda: (
        f"Timed out {target.mention}, their timeout expires {format_timeout_duration(target)}. \n"
        f"Reason: '{reason}'"
    )

    if target.current_timeout is None:
        await target.timeout(until=timeout_duration, reason=reason)
        await inter.send(make_timeout_message())
        return

    await inter.response.defer()

    expiration = disnake.utils.format_dt(target.current_timeout, "R")
    await inter.followup.send(
        f"That user is already timed out. Their timeout expires {expiration}, do you want to overwrite it?",
        components=[
            disnake.ui.Button(label="Yes", style=disnake.ButtonStyle.success, custom_id="yes"),
            disnake.ui.Button(label="No", style=disnake.ButtonStyle.danger, custom_id="no"),
        ]
    )

    try:
        choice: disnake.MessageInteraction = await inter.bot.wait_for(
            "button_click",
            check=lambda i: i.component.custom_id in {"yes", "no"} and i.author.id == inter.author.id,
            timeout=TIMEOUT_PROMPT_WAIT_SECS,
        )

        if choice.component.custom_id == "yes":
            await target.timeout(until=timeout_duration, reason=reason)
            message = make_timeout_message()
        else:
            message = "Canceled."

    except asyncio.TimeoutError:
        message = "No option was chosen, canceled."

    await inter.edit_original_response(message, components=[])


@timeout.sub_command()
async def remove(inter: disnake.GuildCommandInteraction, target: disnake.Member, reason: str):
    """
    Remove timeout from a user

    Parameters
    ----------
    target: The member to remove timeout from
    reason: The reason for the timeout being removed
    """

    hierarchy_check(inter, target)

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
    
    await inter.send(f"{target.mention}'s timeout expires {disnake.utils.format_dt(target.current_timeout, 'R')}")


setup, teardown = plugin.create_extension_handlers()