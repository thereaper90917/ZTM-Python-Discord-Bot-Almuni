###################### ZTM DISCORD BOT #######################
# This project will start off simple and as we progress we can make it more complex with cogs(OOP)

# import discord.py first

# first we need to get the bot to join a discord server
# after we connect to a discord server we will print all the users that join or leave the server
# after this we will start with basic commands
# the first command will be a simple reply from the bot example if we do !ping it should reply "pong"


################ Packages we will be starting with ###################
# Discord.py for documentation refer to  https://discordpy.readthedocs.io/en/latest/


############## IMPORTANT NOTICES WHEN USING DISCORD.PY ####################

# Discord.py was rewritten the latest version is known as (rewrite) due to this i recommend using python 3.7 and up
# to avoid errors/conflicts
import logging
import discord
import todo as db
import os
import requests
from discord.ext import commands, tasks
import praw
import urllib.parse, urllib.request, re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='./discordbot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
client = commands.Bot(command_prefix=commands.when_mentioned_or("!"))


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("The Witcher 3"))
    logging.debug("Bot is ready.")
    print("Bot is Ready. ")


# member has joined server
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')


# member has left server
@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')


# check ping of bot
@client.command()
async def ping(ctx):
    """ Ping times from a bot? """
    await ctx.send(f'Pong! {round(client.latency * 1000)}.ms')


# provide random dad joke
@client.command()
async def dad(ctx):
    """ Returns a random dad joke from icanhazdadjoke.com """
    url = 'https://icanhazdadjoke.com/'
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    joke = response.json()['joke']
    await ctx.send(f'> {joke}')

    
# generate random quote
@client.command()
async def random(ctx):
    """ Returns a random quote """
    url = 'https://api.quotable.io/random'
    response = requests.get(url)
    quote = response.json()
    quote_content = quote['content']
    quote_author = quote['author']
    await ctx.send(f'> {quote_content} \n— {quote_author}')
    
    
#Testing !beginner
@client.command(aliases=['!beginner', '!Beginner'])
async def beginner(ctx):
    """ Gets a set of beginner exercises to work on"""
    await ctx.send(f'Testing beginner')


#Testing !intermediate
@client.command(aliases=['!intermediate', '!Intermediate'])
async def intermediate(ctx):
    await ctx.send(f'Testing intermediate')


#Testing !advanced
@client.command(aliases=['!advanced', '!Advanced'])
async def advanced(ctx):
    """ Gets a set of advanced exercises to work on"""
    await ctx.send(f'Testing advanced')


# Generate top 10 reddit post based on subreddit input
redditclient = praw.Reddit(client_id='WK1IOa7r6-gUGw',
                     client_secret='ZSrUQK_FYoqkhToJetqMjtqjy-I',
                     user_agent='my user agent')

@client.command(aliases=['!reddit'])
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
                                value=f':link:[Link to post]({post.url}) \n:arrow_up: {post.score}  \
                                :speech_left: {post.num_comments}\n',
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


# youtube search capability
@client.command()
async def youtube(ctx, *, search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })

    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string
    )

    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

######################## ZTM DISCORD BOT #########################
# This project will start off simple and as we progress we can make it more complex with cogs(OOP)

# import discord.py first

# first we need to get the bot to join a discord server
# after we connect to a discord server we will print all the users that join or leave the server
# after this we will start with basic commands
# the first command will be a simple reply from the bot example if we do !ping it should reply "pong"


######################## Packages we will be starting with #########################
# Discord.py for documentation refer to  https://discordpy.readthedocs.io/en/latest/


######################## IMPORTAN NOTICES WHEN USING DISCORD.PY #########################

# Discord.py was rewritten the latest version is known as (rewrite) due to this i recommend using python 3.7 and up to avoid errors/conflicts


@client.command()
async def todo(ctx, *args):
    """ Add a needed to-do item to the list of bots needs """
    if len(ctx.args) < 2:
        await ctx.send("Usage: !todo <add/remote/view/update> <task>")
        return

    if ctx.args[1] == 'add':
        search = ctx.message.content.replace('!todo add', '')
        add_data = db.Database("need", search, ctx.author.name, '')
        print(ctx.author.name)
        db.insert_emp(add_data)
        embed = discord.Embed(
            colour=discord.Colour.dark_grey(),
            title="Added the following feature to be done",
            description=f'{search}'
        )
        await ctx.channel.send(embed=embed)

    elif ctx.args[1] == 'view':
        embed = discord.Embed(
            colour=discord.Colour.dark_grey(),
            title="Bot Stuff Needed to be Done",
            description=f'{db.view_data()}'
        )
        await ctx.channel.send(embed=embed)

    elif ctx.args[1] == 'remove':
        input_del = ctx.message.content.replace('!todo remove', '')
        delete_data = db.Database("need", input_del, '', '')
        db.remove_emp(delete_data)
        embed = discord.Embed(
            colour=discord.Colour.dark_grey(),
            title="Deleted the Following",
            description=f'{input_del}'
        )
        await ctx.channel.send(embed=embed)

    elif ctx.args[1] == 'update':
        input_data = ctx.message.content.replace('!todo update', '')
        update_data = db.Database('need', input_data, '', ctx.author)
        db.update_complete(update_data, ctx.author.name)


client.run(os.environ['DISCORD_TOKEN'])  # this uses a OS Environment Variable so the token isn't exposed
