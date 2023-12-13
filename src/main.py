from disnake.ext.commands import InteractionBot
from timeout import TimeoutCommand
from automod import AutoModCommand
from os import environ

bot = InteractionBot()
bot.add_cog(TimeoutCommand(bot))
bot.add_cog(AutoModCommand(bot))

if __name__ == "__main__" and "TOKEN" in environ:
    bot.run(environ["TOKEN"])
