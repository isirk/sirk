import os
from utils.bot import Bot

bot = Bot()

if __name__ == "__main__":
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

    bot.run('NzUxNDQ3OTk1MjcwMTY4NTg2.X1JOew.-sbBb306qsncahZ919jjbYuWn3E')