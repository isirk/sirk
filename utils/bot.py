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

    async def send_log(self, type, message):
        channel = await self.fetch_channel(1159267547582042202)
        time = datetime.datetime.utcnow().strftime("%H:%M:%S")
        if type == "e":
            type = ":exclamation: "
        elif type == "s":
            type = ":gear: "
        elif type == "c":
            type = ":white_check_mark: "
        elif type == "x":
            type = ":x: "
        await channel.send(f"{time} | " + type + message)

    async def on_ready(self):
        await self.send_log("c", f"Connected")

    async def setup_hook(self):
        self.description = (await self.application_info()).description

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    await self.send_log("s", f'Loaded `{filename[:-3]}`')
                except Exception as e:
                    await self.send_log("e", f'Failed to load cog {filename[:-3]}\n```{e}```')

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content == after.content:
            return
        elif after.author.id == self.owner_id:
            await self.process_commands(after)