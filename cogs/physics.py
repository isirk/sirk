import discord, typing
from discord.ext import commands

class physics(commands.Cog):
    '''Commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def engine(self, ctx):
        await ctx.send("Physics Engine")

async def setup(bot):
    await bot.add_cog(physics(bot))