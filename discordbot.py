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

bot = commands.Bot(command_prefix=get_prefix, description='ZTM Python Discord Bot')

# Loading cogs
if __name__ == '__main__':
    for extension in initial_extensions:
        logger.info(f'Loading extension: {extension}')
        bot.load_extension(extension)

@bot.event
async def on_ready():
    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    logger.info('Starting bot...')
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

# Generate top 10 reddit post based on subreddit input
redditclient = praw.Reddit(client_id='Client ID here',
                     client_secret='Secret Client here',
                     user_agent='my user agent')

@bot.command(aliases=['!reddit'])
async def reddit(ctx, arg):
    all_subreddits_url = 'https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits'
    reddit_icon = 'https://cdn2.iconfinder.com/data/icons/social-media-flat-7/64/Social-media_Reddit-512.png'
    if arg == '-help':
        subreddit_list = ['r/coding', 'r/javascript', 'r/programming', 'r/Python', 'r/webdev', 'r/web']

        embed = discord.Embed(title='List of available subreddits', 
                            url=all_subreddits_url, 
                            description="Shows a list of some subreddits where posts can be gotten from\
                            and how to write the commands to get them",
                            color=0x6b57f7)
        embed.set_thumbnail(url=reddit_icon)
        for sub in subreddit_list:
            embed.add_field(name=f'**{sub}**',
                            value=f'!reddit {sub} - Returns top 10 posts in the [{sub}](https://reddit.com/{sub}) subreddit',
                            inline=False)
        embed.add_field(name=f'**All**',
                        value=f'View all available subreddits [here](https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits)\
                        or type !reddit r/all for the top 10 posts from all subreddits combined')
        
        await ctx.send(embed=embed)

    else:
        try:
            hot_posts = redditclient.subreddit(arg[2:]).hot(limit=10)

            embed = discord.Embed(title=f'Top posts in {arg}', 
                                description=f"Shows the hottest posts in the [{arg}](https://reddit.com/{arg}) subreddit",
                                color=0x00ff00)
            embed.set_thumbnail(url=reddit_icon)
            for post in hot_posts:
                embed.add_field(name=f'**{post.title}**',
                                value=f':link:[Link to post]({post.url}) \n:arrow_up: {post.score}  :speech_left: {post.num_comments}',
                                inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f'Sorry, {arg} is not a valid subreddit!\
                            \n\nEnter a valid subreddit name or type **!reddit -help** to get a list of valid subreddits')

@reddit.error
async def reddit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter the name of the subreddit after the **!reddit** command\
                        \n\nType **!reddit -help** for more info on the command')


@bot.command()
async def gn(ctx):
    exit()

bot.run(os.environ['DISCORD_TOKEN'], bot=True, reconnect=True)
