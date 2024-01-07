import disnake
from disnake.ext import plugins, commands


plugin = plugins.Plugin()


@plugin.slash_command()
async def censor(inter: disnake.GuildCommandInteraction):
    pass


# TODO:
@censor.sub_command()
async def rule(inter: disnake.GuildCommandInteraction):
    return


@censor.sub_command_group()
async def word(inter: disnake.GuildCommandInteraction):
    pass


@word.sub_command()
async def block(inter: disnake.GuildCommandInteraction, rule: str, phrases: str, exempt_roles: bool = False, exempt_channels: bool = False, send_alert_message: disnake.TextChannel = None, timeout_user: str = None, custom_message: str = None): # type: ignore
    """
    Block a word from being said in the server

    Parameters
    ----------
    rule: The name of the rule to be made
    phrases: The words to be blocked, seperated by commas
    exempt_roles: Whether or not to exempt users with certain roles from the rule, defaults to none
    exempt_channels: Whether or not to exempt certain channels from the rule, defaults to none
    send_alert_message: The channel to send an alert message to when a user breaks the rule, defaults to none
    timeout_user: The duration to timeout when they break the rule, defaults to no timeout
    custom_message: The custom message to send when a user breaks the rule, defaults to none
    """

    actions_list = []

    if custom_message:
        actions_list.append(disnake.AutoModBlockMessageAction(custom_message=custom_message))
    else:
        actions_list.append(disnake.AutoModBlockMessageAction())

    if send_alert_message:
        actions_list.append(disnake.AutoModSendAlertAction(channel=send_alert_message))

    # if timeout_user:
        # TODO: parse duration of timeout
        
    phrases_list = []

    # Put each phrase into a list
    for phrase in phrases.split(","):
        # Discord API limits phrases to 60 characters
        if len(phrase) > 60:
            raise commands.BadArgument("Phrases must be less than 60 characters long.")
        phrases_list.append(phrase.strip())

    await inter.guild.create_automod_rule(name=rule, trigger_type=disnake.AutoModTriggerType.keyword, event_type=disnake.AutoModEventType.message_send, actions=actions_list, trigger_metadata=disnake.AutoModTriggerMetadata(keyword_filter=phrases_list), enabled=True)
    
    # TODO: Add more info to the embed
    embed = disnake.Embed(title="Rule Created", description=f"Rule {rule} has been created with the following settings:\n\n**Phrases:** {', '.join(phrases_list)}", color=disnake.Color.green())

    await inter.send(embed=embed)


setup, teardown = plugin.create_extension_handlers()