from discord.ext import commands


class Challenges(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
