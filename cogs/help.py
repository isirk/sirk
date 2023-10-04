import discord, difflib
from discord.ext import commands

class HelpCommand(commands.HelpCommand):
    '''Help Command.'''
    def __init__(self):
        super().__init__(command_attrs={
            #'cooldown': commands.Cooldown(1, 3.0, commands.BucketType.member),
            'help': 'Shows help about the bot, a command, or a category',
            "aliases": ["h"]
        })

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Help', description=f'Use `{self.context.clean_prefix}{self.invoked_with} <command/module>` for more help.', colour=self.context.bot.color)
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
        embed.add_field(name='Categories', value=f"```\n{desc}```")
        embed.set_footer(text=self.context.bot.footer)
        #embed.set_footer(text='Use {0}{1} [command|module] for more info.'.format(self.clean_prefix, self.invoked_with))#self.get_ending_note())
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
    
async def setup(bot):
    bot.help_command = HelpCommand()