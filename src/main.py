import asyncio
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import disnake
from disnake.ext import commands

from prisma import Prisma


async def main():
    log_file = Path("../logs/bot.log")
    log_file.parent.mkdir(exist_ok=True)
    
    logging.basicConfig(
        format="%(asctime)s | %(name)s: [%(levelname)s] %(message)s",
        level=logging.INFO,

        handlers=[
            logging.StreamHandler(),
            TimedRotatingFileHandler(
                filename=log_file,
                encoding="utf-8",
                when="midnight",
                utc=True,
                backupCount=7,
            )
        ]
    )

    db = Prisma()
    db.connect()

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