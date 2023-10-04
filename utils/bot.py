import discord, datetime, os
from discord.ext import commands

intents = intents=discord.Intents.default()
intents.message_content = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(      
            command_prefix="^",
            description=None,
            intents=intents, case_insensitive=True, 
            allowed_mentions=discord.AllowedMentions(users=True, roles=True, everyone=False, replied_user=False),
            owner_id=542405601255489537,
        )
        self.uptime = datetime.datetime.utcnow()
        self.footer = "v0.1.1"
        self.color = 0x7289DA
        self.owner = None

    async def send_log(self, message):
        if self.owner is not None:
            await self.owner.send(":gear: | " + message)

    async def on_ready(self):
        await self.send_log(f"Logged in as {self.user}")

    async def setup_hook(self):
        self.owner = await self.fetch_user(self.owner_id)
        self.description = (await self.application_info()).description

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                except Exception as e:
                    await self.send_log(f'Failed to load cog {filename[:-3]}\n{e}')
        await self.send_log('Loaded Cogs')

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content == after.content:
            return
        elif after.author.id == self.owner_id:
            await self.process_commands(after)