import discord
from discord.ext import commands
from dotenv import load_dotenv

import asyncio
import logging
import os
from pathlib import Path

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

LOG_FILE = Path(__file__).resolve().parent.parent / "discord.log"
handler = logging.FileHandler(filename=LOG_FILE, encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

COGS = [
    "cogs.core",
    "cogs.fun",
    "cogs.moderation",
]

async def main():
    discord.utils.setup_logging(handler=handler, level=logging.DEBUG, root=False)

    async with bot:
        for cog in COGS:
            await bot.load_extension(cog)
        await bot.start(TOKEN)

asyncio.run(main())
