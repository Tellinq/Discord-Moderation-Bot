import asyncio
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import disnake
from disnake.ext import commands


async def main():
    logger = logging.getLogger()

    log_file = Path("logs/bot.log")
    log_file.parent.mkdir(exist_ok=True)

    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        utc=True,
        backupCount=7,
        encoding="utf-8"
    )

    file_handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s: [%(levelname)s] %(message)s"))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(name)s: [%(levelname)s] %(message)s"))
    stream_handler.setLevel(logging.WARNING)
    logger.addHandler(stream_handler)

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