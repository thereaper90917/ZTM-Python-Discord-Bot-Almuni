import sqlite3
import discord
from discord.ext import commands


class Database:
    """A sample Employee class"""

    def __init__(self, need, command, complete, completed):
        self.need = need
        self.command = command
        self.complete = complete
        self.completed = completed

    @property
    def user_one(self):
        return '{} {}'.format(self.need, self.command)


class ToDo(commands.Cog):
    """ Cog to add items to a To-do list (broken right now) """
    def __init__(self, bot):
        self.bot = bot
        self.db = '../database.db'
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

    def insert_emp(self, emp):
        with self.conn:
            self.c.execute("INSERT INTO needs VALUES (:need, :command, :complete, :completed)",
                           {'need': emp.need, 'command': emp.command, 'complete': emp.complete, 'completed': emp.completed})

    def remove_emp(self, emp):
        with self.conn:
            self.c.execute("DELETE from needs WHERE need= :need AND command = :command",
                           {'need': emp.need, 'command': emp.command})

    def view_data(self):
        with self.conn:
            self.c.execute("SELECT * FROM needs")
            zlist = []
            items = self.c.fetchall()
            for item in items:
                t = str(item[1]).replace('[', '') + " Created By: " + str(item[2]).replace('[',
                                                                                           '') + ":   Completed By: " + str(
                    item[3]).replace('[', '')
                zlist.append(f'Needed: {t} ')

            new_string = str(zlist).replace("['", "").replace("]", "").replace("', ' ", '\n').replace("', '", '\n')
            return new_string

    def update_complete(self, emp, completed):
        with self.conn:
            self.c.execute("""UPDATE needs SET completed = :completed
                         WHERE need = :need AND command = :command""",
                           {'need': emp.need, 'command': emp.command, 'completed': completed})

    @commands.command(name='todo', aliases=['trello'])
    async def todo(self, ctx, *args):
        """ Add a needed to-do item to the list of bots needs """
        if len(ctx.args) < 2:
            await ctx.send("Usage: !todo <add/remote/view/update> <task>")
            return

        if ctx.args[1] == 'add':
            search = ctx.message.content.replace('!todo add', '')
            add_data = self.db.Database("need", search, ctx.author.name, '')
            print(ctx.author.name)
            self.db.insert_emp(add_data)
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
                description=f'{self.db.view_data()}'
            )
            await ctx.channel.send(embed=embed)

        elif ctx.args[1] == 'remove':
            input_del = ctx.message.content.replace('!todo remove', '')
            delete_data = self.db.Database("need", input_del, '', '')
            self.db.remove_emp(delete_data)
            embed = discord.Embed(
                colour=discord.Colour.dark_grey(),
                title="Deleted the Following",
                description=f'{input_del}'
            )
            await ctx.channel.send(embed=embed)

        elif ctx.args[1] == 'update':
            input_data = ctx.message.content.replace('!todo update', '')
            update_data = self.db.Database('need', input_data, '', ctx.author)
            self.db.update_complete(update_data, ctx.author.name)


def setup(bot):
    bot.add_cog(ToDo(bot))
