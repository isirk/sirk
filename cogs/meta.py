import discord, typing
from discord.ext import commands

class meta(commands.Cog):
    '''Commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        '''Get the bot latency'''
        await ctx.send(f"Pong! Average Latency is {round(self.bot.latency * 1000)} ms")
    
    @commands.command()
    async def id(self, ctx, *, thing: typing.Union[discord.PartialEmoji, discord.Role, discord.Member, discord.TextChannel, discord.VoiceChannel, discord.Emoji]):
        '''Get the id for something'''
        await ctx.send(f"{thing.id}")

    @commands.command()
    async def source(self, ctx):
        '''See the bot's source code'''
        view = discord.ui.View()
        style = discord.ButtonStyle.gray
        item = discord.ui.Button(style=style, label="Source", url="https://youtu.be/dQw4w9WgXcQ")
        view.add_item(item=item)
        await ctx.send("Here is my source!", view=view)

def setup(bot):
    bot.add_cog(meta(bot))