import disnake
from disnake.ext import plugins, commands
import logging

plugin = plugins.Plugin()
logger = logging.getLogger(__name__)


@plugin.listener()
async def on_slash_command_error(inter: disnake.CmdInter, error: commands.CommandError):
    error = getattr(error, "original", error)
    
    log_msg = f"@{inter.author} ran /{inter.application_command.qualified_name} and it failed due to: {error}"
    logger.error(msg=log_msg)
    
    await inter.send(content=str(error), ephemeral=True)


setup, teardown = plugin.create_extension_handlers()