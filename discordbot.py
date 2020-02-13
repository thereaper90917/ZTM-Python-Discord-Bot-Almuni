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
import asyncio
from discord.ext import commands, tasks

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
    
    
@client.command(aliases=['!beginner', '!Beginner'])
async def beginner(ctx):
    await ctx.send(f'Testing beginner')


@client.command(aliases=['!advanced', '!Advanced'])
async def advanced(ctx):
    await ctx.send(f'Testing advanced')


@client.command()
async def reminder(ctx, *args):
    usage = "Set a reminder by using the command !reminder <#minutes> <message>"
    time_scale = {'h': 120,
                  'H': 120,
                  'm': 60,
                  'M': 60,
                  's': 1,
                  'S': 1}

    if len(args) != 2:
        await ctx.send(usage)
        return

    sleep_time = int(args[0])
    reminder_message = args[1]

    await asyncio.sleep(sleep_time)
    await ctx.send(reminder_message)


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
