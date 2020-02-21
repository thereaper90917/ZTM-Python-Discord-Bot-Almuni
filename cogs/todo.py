import sqlite3
import discord
from discord.ext import commands

import praw


class Database:
    def __init__(self, need, command, complete, completed, working):
        self.need = need
        self.command = command
        self.complete = complete
        self.completed = completed
        self.working = working
        
    @property
    def user_one(self):
        return '{} {}'.format(self.need, self.command)



class Test(commands.Cog):
    """ Cog to add items to a To-do list (broken right now) """
    def __init__(self, bot):
        self.bot = bot
        self.db = '../database.db'
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

    def insert_emp(self, emp):
        with self.conn:
            self.c.execute("INSERT INTO needs VALUES (:need, :command, :complete, :completed, :working)",
                           {'need': emp.need, 'command': emp.command, 'complete': emp.complete, 'completed': emp.completed, 'working':emp.working})

    def remove_emp(self, emp):
        with self.conn:
            self.c.execute("DELETE from needs WHERE need= :need AND command = :command",
                           {'need': emp.need, 'command': emp.command})

    def update_complete(self, emp, completed):
        with self.conn:
            self.c.execute("""UPDATE needs SET completed = :completed
                         WHERE need = :need AND command = :command""",
                           {'need': emp.need, 'command': emp.command, 'completed': completed})


    def update_done(self, emp, done):
        with self.conn:
            self.c.execute("""UPDATE needs SET working = :working
                         WHERE need = :need AND command = :command""",
                           {'need': emp.need, 'command': emp.command, 'working': done})

    @commands.command(name='todo')
    async def todo(self, ctx, *args):
        """ Add a needed to-do item to the list of bots needs """
        if len(args) < 2:
            await ctx.send("Usage: !todo <add/remote/view/update> <task>")
            print("working")

        if 'add' in args:
            search = ctx.message.content.replace('!todo add', '')
            add_data = Database("need", search, ctx.author.name, '','')
            self.insert_emp(add_data)
            embed = discord.Embed(
                colour=discord.Colour.dark_grey(),
                title="Added the following feature to be done",
                description=f'{search}'
            )
            await ctx.channel.send(embed=embed)

        elif 'view' in args:
            embed = discord.Embed(
                colour=discord.Colour.dark_grey()
            )
            embed.set_author(name="Commands Being Worked On")
            #embed.add_field(name=f'{self.view_data()}',value='testing', inline=True)
            with self.conn:
                self.c.execute("SELECT * FROM needs")
                items = self.c.fetchall()
                for item in items:
                    t = str(item[1]).replace('[', '')

                    y = str(item[2]).replace('[','')

                    n =  str(item[3]).replace('[', '')

                    w =  str(item[4]).replace('[', '')
                    embed.add_field(name=f'Need: {t}',value=f'Created By: {y} \n Completed By: {n} \n Worked on By: {w}', inline=False)

                await ctx.channel.send(embed=embed)

        elif 'remove' in args:
            input_del = ctx.message.content.replace('!todo remove', '')
            delete_data = Database("need", input_del, '', '','')
            self.remove_emp(delete_data)
            embed = discord.Embed(
                colour=discord.Colour.dark_grey(),
                title="Deleted the Following",
                description=f'{input_del}'
            )
            await ctx.channel.send(embed=embed)

        elif 'update' in args:
            input_data = ctx.message.content.replace('!todo update', '')
            update_data = Database('need', input_data, '', ctx.author,'')
            self.update_complete(update_data, ctx.author.name)
         
        elif 'complete' in args:
            input_data = ctx.message.content.replace('!todo complete', '')
            update_data = Database("need", input_data, '', '',ctx.author)
            self.update_done(update_data, ctx.author.name)


def setup(bot):
    bot.add_cog(Test(bot))
