import requests
from bs4 import BeautifulSoup
from hyper.contrib import HTTP20Adapter
from discord.ext import commands


class Challenges(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://www.hackerrank.com/domains/python'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
        self.get_results()


    def create_links(self, links, rank):
        hn = []
        for idx, item in enumerate(links):
            title = item.getText()
            href = item.get('href', None)
            vote = rank[idx].select('.difficulty')
            if len(vote):
                r = int(vote[0].getText().replace(' points', ''))
                if r == rank:
                    hn.append({'title': title, 'link': href, 'votes': points})
        return hn

    def get_results(self):
        conn = requests.Session()
        conn.mount('https://', HTTP20Adapter())
        resp = conn.get(self.url, headers=self.headers)
        soup = BeautifulSoup(resp.content, 'html.parser')
        links = soup.select('.challenge-list-item')
        rank = soup.select('.difficulty')
        print(enumerate(links))

    @commands.command(name='beginner', aliases=['Beginner'])
    async def beginner(self, ctx):
        """ Gets a set of beginner exercises to work on"""
        await ctx.send(f'Testing beginner')

    @commands.command(name='intermediate', aliases=['!intermediate', '!Intermediate'])
    async def intermediate(self, ctx):
        """ Gets a set of intermediate exercises to work on"""
        await ctx.send(f'Testing intermediate')

    @commands.command(name='advanced', aliases=['!advanced', '!Advanced'])
    async def advanced(self, ctx):
        """ Gets a set of advanced exercises to work on"""
        await ctx.send(f'Testing advanced')


def setup(bot):
    bot.add_cog(Challenges(bot))
