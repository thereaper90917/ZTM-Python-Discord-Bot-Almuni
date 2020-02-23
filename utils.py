import json
from discord.ext import commands

CONFIG_FILE = 'discordbot.config'


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Add prefixes that you want the bot to respond to
    prefixes = ['?', '!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


def read_config(blob=None):
    """ Returns a config_file['blob] from requesting cogs or config_file to bot """
    with open(CONFIG_FILE, 'r') as config_json:
        config = json.load(config_json)
    config_json.close()

    if blob:
        return config[blob]
    return config
