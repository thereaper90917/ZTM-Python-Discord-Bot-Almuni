import re
from urllib import parse, request
from discord.ext import commands


class YouTube(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='yt-search')
    async def search_youtube(self, ctx, *, search):
        """ Search youtube for videos """
        query_string = parse.urlencode({
            'search_query': search
        })

        htm_content = request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )

        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
        await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])


def setup(bot):
    bot.add_cog(YouTube(bot))
