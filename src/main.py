import asyncio
import logging
import os

import disnake
from disnake.ext import commands


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s',
        
        handlers=[
            logging.StreamHandler(), 
            logging.FileHandler("bot.log", mode="w", encoding="utf-8")]
    )

    bot = commands.InteractionBot(
        reload=True,
        intents=disnake.Intents.all(),
        test_guilds=[1187465948505063597]
    )
    
    bot.load_extensions("exts/commands")
    bot.load_extensions("exts/listeners")
    await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())