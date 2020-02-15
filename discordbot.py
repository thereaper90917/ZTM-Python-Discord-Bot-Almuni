import discord
import sqlite3
from database_user import Database
import os
import requests
from discord.ext import commands, tasks
import praw
import urllib.parse, urllib.request, re

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
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# generate random quote
@client.command()
async def random(ctx):
    url = 'https://api.quotable.io/random'
    response = requests.get(url)
    quote = response.json()
    quote_content = quote['content']
    quote_author = quote['author']
    await ctx.send(f'> {quote_content} \n— {quote_author}')



# provide random dad joke
@client.command()
async def dad(ctx):
    url = 'https://icanhazdadjoke.com/'
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    joke = response.json()['joke']
    await ctx.send(f'> {joke}')

#Testing !beginner
@client.command(aliases=['!beginner', '!Beginner'])
async def beginner(ctx):
    await ctx.send(f'Testing beginner')


#Testing !advanced
@client.command(aliases=['!advanced', '!Advanced'])
async def advanced(ctx):
    await ctx.send(f'Testing advanced')


#Testing !intermediate
@client.command(aliases=['!intermediate', '!Intermediate'])
async def intermediate(ctx):
    await ctx.send(f'Testing intermediate')


# Generate top 6 reddit post based on subreddit input
@client.command(aliases=['reddit'])
async def _beginner(ctx, *args):
    response = ''
    size = 6
    length = len(args)
    arg = 'random'

    if length > 0:
        arg = args[0]

    reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                         client_secret=os.environ['CLIENT_SECRET'],
                         user_agent='my user agent')

    response = 'Top Ten ' + arg + ' Subrredit Posts \n--------------------------------------\n'

    try:
        for submission in reddit.subreddit(arg).hot(limit=size):
            # print(submission.title)
            response = response + '\n' + submission.title + '\n<' + submission.url + '>' + '\n'

    except Exception as e:
        # print(e)
        response = arg + ' is not a valid subreddit!'


    await ctx.send(f'{response}')


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

############################################### TRELLO CLONE ###################################################
@client.event
async def on_message(message):
     conn = sqlite3.connect('database.db')#if you get an error please use absolute/explicit path example C:\discord\database.db

     c = conn.cursor()


     def insert_emp(emp):
         with conn:
            c.execute("INSERT INTO needs VALUES (:need, :command, :complete, :completed)", {'need': emp.need, 'command': emp.command, 'complete':emp.complete,'completed':emp.completed})


     def remove_emp(emp):
         with conn:
            c.execute("DELETE from needs WHERE need= :need AND command = :command",
                  {'need': emp.need, 'command': emp.command})
     def view_data():
        with conn:
            c.execute("SELECT * FROM needs")
            zlist =[]
            items =  c.fetchall()
            for item in items:
                t = str(item[1]).replace('[','') +" Created By: " + str(item[2]).replace('[','') + ":   Completed By: "+ str(item[3]).replace('[','')
                zlist.append(f'Needed: {t} ')

            new_string=str(zlist).replace("['","").replace("]","").replace("', ' ",'\n').replace("', '",'\n')
            return new_string

     def update_complete(emp, completed):
            with conn:
                    c.execute("""UPDATE needs SET completed = :completed
                         WHERE need = :need AND command = :command""",
                    {'need': emp.need, 'command': emp.command, 'completed': completed})


     if message.author.bot:
        return
     if message.content.startswith('!add'):
        search = message.content.replace('!add','')
        add_data = Database("need",search ,message.author.name,'')
        print(message.author.name)
        insert_emp(add_data)
        embed = discord.Embed(
        colour = discord.Colour.dark_grey(),
        title = ("Added the following feature to be done"),
        description= (f'{search}')
            )
        await message.channel.send(embed=embed)

     if message.content.startswith('!view'):
        embed = discord.Embed(
        colour = discord.Colour.dark_grey(),
        title = ("Bot Stuff Needed to be Done"),
        description= (f'{view_data()}')
            )
        await message.channel.send(embed=embed)

     if message.content.startswith('!remove'):
            input_del = message.content.replace('!remove','')
            delete_data = Database("need",input_del,'', '')
            remove_emp(delete_data)
            embed = discord.Embed(
            colour = discord.Colour.dark_grey(),
            title = ("Deleted the Following"),
            description= (f'{input_del}')
                )
            await message.channel.send(embed=embed)


     if message.content.startswith('!update'):
            input_data = message.content.replace('!update','')
            update_data = Database('need',input_data,'',message.author)
            update_complete(update_data,message.author.name)





     await client.process_commands(message)


client.run(os.environ['DISCORD_TOKEN'])  # this uses a OS Environment Variable so the token isn't exposed
