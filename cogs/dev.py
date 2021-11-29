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
            self.bot.load_extension(f"cogs.{name}")
            await ctx.message.add_reaction('📥')
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")

    @commands.command(aliases=['r'])
    async def reload(self, ctx, name: str):
        """Reloads an extension. """
        try:
            self.bot.reload_extension(f"cogs.{name}")
            await ctx.message.add_reaction('🔁')
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")

    @commands.command()
    async def unload(self, ctx, name: str):
        """Unloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
            await ctx.message.add_reaction('📤')
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")
    
    @commands.command(aliases=['ra'])
    async def reloadall(self, ctx):
        """Reloads all extensions. """
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"cogs.{name}")
                except Exception as e:
                    return await ctx.send(f"```py\n{e}```")

        if error_collection:
            output = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
            return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

        await ctx.message.add_reaction('🔁')

    @commands.command()
    async def exit(self, ctx):
        try:
            await ctx.message.add_reaction('👋')
        except:
            pass
        await self.bot.close()

def setup(bot):
    bot.add_cog(dev(bot))