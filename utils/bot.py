import discord, datetime
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(        
            command_prefix="^",
            intents=discord.Intents.default(), case_insensitive=True, 
            allowed_mentions=discord.AllowedMentions(users=True, roles=True, everyone=False, replied_user=False),
            owner_id=542405601255489537,
        )
        self.uptime = datetime.datetime.utcnow()
        self.footer = "Sirk Bot v1"
        self.color = 0x7289DA

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content == after.content:
            return
        elif after.author.id == self.owner_id:
            await self.process_commands(after)