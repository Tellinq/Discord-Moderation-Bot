import logging
import os

import disnake
from disnake.ext import commands

def main():

    logger = logging.getLogger("disnake")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename="disnake.log", encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
    logger.addHandler(handler)

    bot = commands.InteractionBot(
        reload=True, # Hot reloading, only use for dev testing
        intents=disnake.Intents.all(),
        test_guilds=[1184304033834467440]
    )

    @bot.event
    async def on_ready():
        print(f"Sucessfully logged in as {bot.user.name}.\n")
        
    os.chdir(os.path.dirname(__file__))
    bot.load_extensions("cogs")
    
    bot.run(os.environ["TOKEN"])


if __name__ == "__main__":
    main()