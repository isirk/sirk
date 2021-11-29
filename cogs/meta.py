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

    @commands.command(aliases=['about'])
    async def info(self, ctx):
        '''See information about the bot'''
        embed = discord.Embed(title=self.bot.user.name, description="a bot", color=self.bot.color)
        embed.add_field(name=f"Stats", value=f"Ping: {round(self.bot.latency * 1000)} ms\nServers: {len(self.bot.guilds)}\nCommands: {len(self.bot.commands)}")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=self.bot.footer)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(meta(bot))