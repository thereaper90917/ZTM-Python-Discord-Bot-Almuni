import discord
from discord.ext import commands
import praw
import logging
import os

logger = logging.getLogger('reddit')


class Reddit(commands.Cog):
    """ Reddit actions """

    def __init__(self, bot):
        self.bot = bot
        self.login = praw.Reddit(client_id=os.environ['REDDIT_ID'],
                                 client_secret=os.environ['REDDIT_SECRET'],
                                 user_agent=os.environ['REDDIT_UA'])

    @commands.command(name='reddit')
    async def do_reddit(self, ctx, args):
        author = ctx.message.author
        all_subreddits_url = 'https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits'
        reddit_icon = 'https://cdn2.iconfinder.com/data/icons/social-media-flat-7/64/Social-media_Reddit-512.png'
        if args == '-help':
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
                hot_posts = self.login.subreddit(args[2:]).hot(limit=10)

                embed = discord.Embed(title=f'Top posts in {args}',
                                      description=f"Shows the hottest posts in the [{args}](https://reddit.com/{args}) subreddit",
                                      color=0x00ff00)
                embed.set_thumbnail(url=reddit_icon)
                for post in hot_posts:
                    embed.add_field(name=f'**{post.title}**',
                                    value=f':link:[Link to post]({post.url}) \n:arrow_up: {post.score}  :speech_left: {post.num_comments}',
                                    inline=False)

                await ctx.send(embed=embed)
                logger.info(f'{author.name} ({author.id}) requested info {args}')
            except Exception as e:
                logger.error(f'An error occurred, Args= {args}, Error= {e}')
                await ctx.send(f'Sorry, {args} is not a valid subreddit!\
                    \n\nEnter a valid subreddit name or type **!reddit -help** to get a list of valid subreddits')

    @do_reddit.error
    async def reddit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please enter the name of the subreddit after the **!reddit** command\
                            \n\nType **!reddit -help** for more info on the command')


def setup(bot):
    if logger.level == 0:  # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename='logs/reddit.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    bot.add_cog(Reddit(bot))
