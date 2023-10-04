import asyncio
from utils.bot import Bot

bot = Bot()

async def main():
    async with bot:
        await Bot().start("MTE0NjIxNjc1NTcxOTU4MTcyNg.G85lpK.4DefYimkxgHenc53dbfNRirE5szQjAmGkCzGGc")

asyncio.run(main())