import discord
from discord.ext import commands

class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            embed = discord.Embed(
                title = "An error occurred!",
                description = f"```{str(error)}```",
                color = discord.Color.red()
            )
            embed.set_footer(text=self.bot.footer)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(error(bot))