import disnake
from disnake.ext import plugins, commands


plugin = plugins.Plugin()


@plugin.listener()
async def on_slash_command_error(inter: disnake.CmdInter, error: commands.CommandError):
    await inter.send(error, ephemeral=True)


setup, teardown = plugin.create_extension_handlers()