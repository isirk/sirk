import discord, difflib, datetime
from discord.ext import commands

class HelpCommand(commands.HelpCommand):
    '''Help Command.'''
    def __init__(self):
        super().__init__(command_attrs={
            'help': 'Shows help about the bot, a command, or a category',
            "aliases": ["h"]
        })

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Help', description=f'Use `{self.context.clean_prefix}{self.invoked_with} <module>` for more help.', colour=self.context.bot.color)
        cogs = []
        for cog, commands in mapping.items():
            if cog is None:
                pass
            else:
                filtered = await self.filter_commands(commands, sort=True)
                if filtered:
                    #embed.add_field(name=cog.qualified_name.capitalize(), value=" ".join(f"`{command}`" for command in await self.filter_commands(cog.get_commands())) or "No commands")
                    cogs.append(cog.qualified_name)
        desc = '\n'.join(cogs)
        embed.add_field(name='Modules', value=f"```\n{desc}```")
        embed.set_footer(text=self.context.bot.footer)
        return await self.context.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"{self.context.clean_prefix}{command.name} | {' | '.join(command.aliases)} {command.signature}" if len(command.aliases) > 0 else f'{self.context.clean_prefix}{command.name} {command.signature}',
                              description=command.help or "No info available.",
                              colour=self.context.bot.color)
        embed.set_footer(text=self.context.bot.footer)
        return await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.qualified_name.capitalize(),
                              description=" ".join(f"`{command}`" for command in await self.filter_commands(cog.get_commands())) or "No commands",
                              colour=self.context.bot.color)
        embed.set_footer(text=self.context.bot.footer)
        return await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group.name.capitalize(),
                              description=" ".join(f"`{command}`" for command in await self.filter_commands(group.walk_commands())) or "None",
                              colour=self.context.bot.color)
        if group.aliases:
            embed.add_field(name="Aliases:", value="\n".join(group.aliases), inline=False)
        embed.set_footer(text=self.context.bot.footer)
        return await self.context.send(embed=embed)

    async def command_not_found(self, string):
        command_names = [str(x) for x in self.context.bot.commands]
        matches = difflib.get_close_matches(string, command_names)
        if matches:
            return f"The command `{string}` was not found, did you mean... `{matches[0]}`?"
        else:
            return f"The command `{string}` was not found."

class core(commands.Cog):
    '''Commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            embed = discord.Embed(
                description = f"```{str(error)}```",
                color = discord.Color.red()
            )
            embed.set_footer(text=self.bot.footer)
            await ctx.send(embed=embed)

    @commands.command(aliases=['about'])
    async def info(self, ctx):
        '''See information about the bot'''
        uptime = str(datetime.datetime.utcnow() - self.bot.uptime)
        embed = discord.Embed(title=self.bot.user.name, description=self.bot.description, color=self.bot.color)
        embed.add_field(name=f"Stats", value=f"Ping: `{round(self.bot.latency * 1000)} ms`\nUptime: `{uptime.split('.')[0]}`\nServers: `{len(self.bot.guilds)}`\nCommands: `{len(self.bot.commands)}`")
        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.set_footer(text=self.bot.footer)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(core(bot))
    bot.help_command = HelpCommand()