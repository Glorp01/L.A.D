import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("lad")

intents = discord.Intents.default()
intents.message_content = True


class LADBot(commands.Bot):
    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                log.info("Loaded cog: %s", filename)
        synced = await self.tree.sync()
        log.info("Synced %d slash command(s)", len(synced))


bot = LADBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    log.info("Logged in as %s (ID: %s)", bot.user, bot.user.id)


def main():
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN not set. Copy .env.example to .env and fill it in.")
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
