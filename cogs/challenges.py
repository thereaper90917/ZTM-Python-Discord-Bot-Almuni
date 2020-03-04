import requests
import random
import discord
from bs4 import BeautifulSoup
from hyper.contrib import HTTP20Adapter
from discord.ext import commands


class Challenges(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.site = 'https://www.hackerrank.com'
        self.url_path = '/domains/python'
        self.url = self.site + self.url_path
        self.url_args = '?filters%5Bdifficulty%5D%5B%5D='
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
        self.difficulties = ['Easy', 'Medium', 'Hard']

    def create_links(self, links, ranks, difficulty):
        results = []
        for idx, item in enumerate(links):
            title = item.find('h4', class_='challengecard-title').get_text()
            i = title.find(difficulty)
            title = title[:i]
            href = self.site + item.get('href', None)
            r = ranks[idx].getText()
            if len(difficulty):
                if r == difficulty:
                    results.append({'title': title, 'link': href, 'rank': difficulty})
        return results

    # TODO: Paginate the website and get all challenges
    def get_results(self, difficulty):
        challenges = []
        conn = requests.Session()
        conn.mount('https://', HTTP20Adapter())
        if difficulty in self.difficulties:
            url = self.url + self.url_args + str.lower(difficulty)
            resp = conn.get(url, headers=self.headers)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'html.parser')
                links = soup.select('.challenge-list-item')
                ranks = soup.select('.difficulty')
                challenges += self.create_links(links, ranks, difficulty)
        return challenges

    @staticmethod
    def create_embed(results):
        r = random.choice(results)
        embed = discord.Embed(
            colour=discord.Colour.dark_grey(),
            title=f"{r['title']} | Difficulty: {r['rank']}",
            description=f"{r['link']}"
        )
        return embed

    @commands.command(name='beginner', aliases=['Beginner'])
    async def beginner(self, ctx):
        """ Gets a set of beginner exercises to work on"""
        results = self.get_results('Easy')
        embed = self.create_embed(results)
        await ctx.send(embed=embed)

    @commands.command(name='intermediate', aliases=['!intermediate', '!Intermediate'])
    async def intermediate(self, ctx):
        """ Gets a set of intermediate exercises to work on"""
        results = self.get_results('Medium')
        embed = self.create_embed(results)
        await ctx.send(embed=embed)

    @commands.command(name='advanced', aliases=['!advanced', '!Advanced'])
    async def advanced(self, ctx):
        """ Gets a set of advanced exercises to work on"""
        results = self.get_results('Hard')
        embed = self.create_embed(results)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Challenges(bot))
