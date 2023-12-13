from nextcord.ext.commands import Bot
from timeout import Timeout
from os import environ

bot = Bot()
bot.add_cog(Timeout(bot))

if __name__ == "__main__" and "TOKEN" in environ:
    bot.run(environ["TOKEN"])