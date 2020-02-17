import praw
from discord.ext import commands


class Reddit(commands.Cog):
    """ Reddit actions """

    def __init__(self, bot):
        self.bot = bot
        self.login = praw.Reddit(client_id='WK1IOa7r6-gUGw',
                                 client_secret='ZSrUQK_FYoqkhToJetqMjtqjy-I',
                                 user_agent='my user agent')

    @commands.command(name='reddit')
    async def do_reddit(self, ctx, *args):
        """ Generate top 6 reddit post based on subreddit input """
        response = ''
        size = 6
        length = len(args)
        arg = 'random'

        if length > 0:
            arg = args[0]

        response = 'Top Ten ' + arg + ' Subrredit Posts \n--------------------------------------\n'

        try:
            for submission in reddit.subreddit(arg).hot(limit=size):
                # print(submission.title)
                response = response + '\n' + submission.title + '\n<' + submission.url + '>' + '\n'

        except Exception as e:
            # print(e)
            response = arg + ' is not a valid subreddit!'

        await ctx.send(f'{response}')


def setup(bot):
    bot.add_cog(Reddit(bot))
