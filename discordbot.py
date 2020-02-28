import discord
import logging
from discord.ext import commands
import utils
import sys
import os

CONFIG_FILE = 'discordbot.config'

options = utils.get_opts(sys.argv[1:])

if not utils.check_dir('logs'):
    os.mkdir('logs')
else:
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)   # Change this to get DEBUG info if necessary
    handler = logging.FileHandler(filename='logs/discordbot.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


if options.config:
    config = utils.read_config(file=options.config)
else:
    config = utils.read_config()
logger.info(f'Reading Configuration file: {config}')


logger.info('Starting bot...')
bot = commands.Bot(command_prefix=utils.get_prefix, description=config['description'])

# Loading cogs
if __name__ == '__main__':
    for extension in config['modules']:
        logger.info(f'Loading extension: {extension}')
        bot.load_extension(extension)


@bot.event
async def on_ready():
    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Game(name='The Witcher 3'))
    print(f'Successfully logged in and booted...!')
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


# member has joined server
@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server')


# member has left server
@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server')


@bot.command()
async def gn(ctx):
    exit()

bot.run(config['token'], bot=True, reconnect=True)
