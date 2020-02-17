import discord
import requests
from discord.ext import commands


class Random(commands.Cog):
    """ Random actions Cog """

    def __init__(self, bot):
        self.bot = bot

    # provide random dad joke
    @commands.command(name='dad', aliases=['joke'])
    async def do_dad(self, ctx):
        """ Returns a random dad joke from icanhazdadjoke.com """
        url = 'https://icanhazdadjoke.com/'
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        joke = response.json()['joke']
        await ctx.send(f'> {joke}')

    # generate random quote
    @commands.command(name='random', aliases=['quote'])
    async def do_random(self, ctx):
        """ Returns a random quote """
        url = 'https://api.quotable.io/random'
        response = requests.get(url)
        quote = response.json()
        quote_content = quote['content']
        quote_author = quote['author']
        await ctx.send(f'> {quote_content} \n— {quote_author}')

    @commands.command(name='ping')
    async def ping(self, ctx):
        """ Ping times from a bot? """
        await ctx.send(f'Pong! {round(client.latency * 1000)}.ms')


def setup(bot):
    bot.add_cog(Random(bot))
