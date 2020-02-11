import discord
import os
import requests
from discord.ext import commands, tasks

client = commands.Bot(command_prefix=commands.when_mentioned_or("!"))


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("The Witcher 3"))
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
    await ctx.send(f'Pong! {round(client.latency * 1000)}.ms')


# provide random dad joke
@client.command()
async def dad(ctx):
    url = 'https://icanhazdadjoke.com/'
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    joke = response.json()['joke']
    await ctx.send(f'> {joke}')


# generate random quote
@client.command()
async def random(ctx):
    url = 'https://api.quotable.io/random'
    response = requests.get(url)
    quote = response.json()
    quote_content = quote['content']
    quote_author = quote['author']
    await ctx.send(f'> {quote_content} \n— {quote_author}')


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

client.run(os.environ['DISCORD_TOKEN'])  # this uses a OS Environment Variable so the token isn't exposed
