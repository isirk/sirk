import discord, inspect, io, textwrap, traceback, os
from discord.ext import commands
from contextlib import redirect_stdout

class dev(commands.Cog):
    '''Developer Commands'''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.NotOwner
        return True

    @commands.command()
    async def load(self, ctx, name: str):
        """Loads an extension. """
        try:
            await self.bot.load_extension(f"cogs.{name}")
            await ctx.message.add_reaction('📥')
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")

    @commands.command(aliases=['r'])
    async def reload(self, ctx, name: str):
        """Reloads an extension. """
        try:
            await self.bot.reload_extension(f"cogs.{name}")
            await ctx.message.add_reaction('🔁')
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")

    @commands.command()
    async def unload(self, ctx, name: str):
        """Unloads an extension. """
        try:
            await self.bot.unload_extension(f"cogs.{name}")
            await ctx.message.add_reaction('📤')
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")
    
    @commands.command(aliases=['ra'])
    async def reloadall(self, ctx):
        """Reloads all extensions. """
        
        self.bot.description = (await self.bot.application_info()).description

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.bot.reload_extension(f'cogs.{filename[:-3]}')
                except Exception as e:
                    await ctx.send(f'Failed to load cog {filename[:-3]}\n{e}')        
        await ctx.message.add_reaction('🔁')

    @commands.command()
    async def exit(self, ctx):
        try:
            await ctx.message.add_reaction('👋')
        except:
            pass
        await self.bot.close()

    @commands.command()
    async def cogs(self, ctx):
        cogs = "\n".join([cog for cog in self.bot.cogs])
        await ctx.send(embed=discord.Embed(description=f"```{cogs}```", color=self.bot.color))

async def setup(bot):
    await bot.add_cog(dev(bot))