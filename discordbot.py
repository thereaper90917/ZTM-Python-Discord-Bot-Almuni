import discord
import os
import logging
from discord.ext import commands

global logger
logger = logging.getLogger('discord')
if logger.level == 0:               # Prevents the logger from being loaded again in case of module reload
    logger.setLevel(logging.INFO)   # Change this to get DEBUG info if necessary
    handler = logging.FileHandler(filename='logs/discordbot.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['?', '!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Cogs need to be located in cogs folder and added here to load on startup
initial_extensions = ['cogs.random',
                      'cogs.reddit',
                      'cogs.youtube',
                      'cogs.todo',
                      'cogs.challenges']

logger.info('Starting bot...')
bot = commands.Bot(command_prefix=get_prefix, description='ZTM Python Discord Bot')

# Loading cogs
if __name__ == '__main__':
    for extension in initial_extensions:
        logger.info(f'Loading extension: {extension}')
        bot.load_extension(extension)


@bot.event
async def on_ready():
    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Game(name='The Witcher 3'))
    print(f'Successfully logged in and booted...!')
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    logger.info('Bot started.')


# member has joined server
@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server')


# member has left server
@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server')

bot.run(os.environ['DISCORD_TOKEN'], bot=True, reconnect=True)
