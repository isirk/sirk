import asyncio, os
from utils.bot import Bot

bot = Bot()

async def main():
    async with bot:
        await bot.start(os.environ.get("DISCORD_TOKEN"))

asyncio.run(main())