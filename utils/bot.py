import discord, datetime, os, jishaku
from discord.ext import commands

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

intents = intents=discord.Intents.default()
intents.message_content = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(        
            command_prefix="^",
            intents=intents, case_insensitive=True, 
            allowed_mentions=discord.AllowedMentions(users=True, roles=True, everyone=False, replied_user=False),
            owner_id=542405601255489537,
        )
        self.uptime = datetime.datetime.utcnow()
        self.footer = "Sirk Bot v1"
        self.color = 0x7289DA
        self.owner = None

    async def send_log(self, message):
        if self.owner is not None:
            await self.owner.send(":gear: | " + message)

    async def on_ready(self):
        await self.send_log(f"Logged in as {self.user}")

    async def setup_hook(self):
        self.owner = await self.fetch_user(self.owner_id)
        await self.load_extension('jishaku')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        await self.send_log('Loaded Cogs')

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content == after.content:
            return
        elif after.author.id == self.owner_id:
            await self.process_commands(after)