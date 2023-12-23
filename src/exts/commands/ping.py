import disnake
from disnake.ext import plugins


plugin = plugins.Plugin()


@plugin.slash_command()
async def ping(inter: disnake.CmdInter):
    """Get the bot's current websocket latency"""
    await inter.send(f"Pong! {round(plugin.bot.latency * 1000)}ms")


setup, teardown = plugin.create_extension_handlers()