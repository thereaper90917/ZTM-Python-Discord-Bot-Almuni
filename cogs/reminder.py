import discord
from discord.ext import commands
import asyncio
import time
import logging
from tinydb import TinyDB

logger = logging.getLogger("reminders")


class Reminder(commands.Cog):
    """ Set a Reminder for text in given amount of time """

    def __init__(self, bot, loop=asyncio):
        self.bot = bot
        self.reminders = TinyDB('data/reminders.db')
        self.units = {"m": 60,
                      "h": 3600,
                      "d": 86400,
                      "w": 604800}
        self.times = ['minute', 'hour', 'day', 'week']
        self.loop = asyncio.get_event_loop()
        self.bg_task = self.loop.create_task(self.do_reminder())

    def add_db(self, data):
        # TODO: Fix this...
        try:
            self.reminders.insert(data)
            return True
        except Exception as e:
            return False

    def rm_db(self, rec):
        # TODO: Encapsulate db code in to rm_db()
        pass

    def view_db(self, user_id):
        # TODO: Encapsulate viewing of db records in to view_db()
        pass

    @commands.command(pass_context=True, aliases=['reminders', 'set_reminder', 'add_reminder'])
    async def reminder(self, ctx, quantity: int, time_unit: str, *, text: str):
        """Set a reminder - Usage: !reminder <int> <minutes/hours/days/weeks> <reminder message"""
        time_prefix = time_unit.lower()[:1]
        author = ctx.message.author
        s = ''

        if time_unit.endswith("s"):
            time_unit = time_unit[:-1]
            s = "s"
        if time_unit not in self.times:
            await ctx.send("Invalid time unit. Choose minutes/hours/days/weeks/month")
            return
        if not quantity or quantity < 1:
            await ctx.send("Quantity must not be 0 or negative.")
            return
        if len(text) > 1960:
            await ctx.send("Text is too long.")
            return
        seconds = self.units[time_prefix] * quantity
        future = int(time.time() + seconds)
        data = {"id": author.id,
                "remind_at": future,
                "time": str(quantity) + ' ' + time_unit,
                "message": text}
        if self.reminders.insert(data):
            logger.info(f"{author.name} ({author.id}) set a reminder.")
            await ctx.send(f"I will remind you of that in {str(quantity)} {time_unit}{s}.")
        else:
            await ctx.send("Something went wrong.")

    @reminder.error
    async def reminder_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must supply the correct arguments")
            logger.error(f'An error occurred: {error} - {ctx.message.author}')

    @commands.command(pass_context=True)
    async def clear_reminders(self, ctx):
        """Removes all your upcoming reminders"""
        author = ctx.message.author
        removable = []
        for reminder in self.reminders:
            if reminder["id"] == author.id:
                removable.append(reminder)

        if not removable == []:
            for item in removable:
                self.reminders.remove(doc_ids=[item.doc_id])
            await ctx.send("Your reminders have been cleared")
            logger.info(f"{author.name} ({author.id}) cleared all reminders.")
        else:
            await ctx.send("You don't have any reminders.")

    @commands.command(pass_context=True)
    async def view_reminders(self, ctx):
        """View all your upcoming reminders"""
        author = ctx.message.author
        id_list = []
        time_list = []
        msg_list = []

        if len(self.reminders) > 0:
            for reminder in self.reminders:
                if reminder['id'] == author.id:
                    id_list.append(str(reminder.doc_id))
                    time_list.append(reminder['time'])
                    msg_list.append(reminder['message'])
                else:
                    return
            embed = discord.Embed(colour=discord.Colour.dark_grey(), title="Reminders")
            embed.add_field(name='#',
                            value=str(id_list).replace(',', '\n').replace('[', '').replace(']', '').replace('\'', ''),
                            inline=True)
            embed.add_field(name='Time',
                            value=str(time_list).replace(',', '\n').replace('[', '').replace(']', '').replace('\'', '') + 's',
                            inline=True)
            embed.add_field(name='Reminder',
                            value=str(msg_list).replace(',', '\n').replace('[', '').replace(']', '').replace('\'', ''),
                            inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Reminder database is empty")

    async def do_reminder(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            to_remove = []
            if len(self.reminders) > 0:
                for reminder in self.reminders:
                    if reminder["remind_at"] <= int(time.time()):
                        user = await self.bot.fetch_user(int(reminder['id']))
                        dm_channel = user.dm_channel
                        if not dm_channel:
                            dm_channel = await user.create_dm()
                            print(dm_channel)
                        await dm_channel.send(f"You asked me to remind you with this message:\n{reminder['message']}")
                        to_remove.append(reminder.doc_id)
                        logger.info(f"{user.name} ({user.id}) reminder sent at {time.time()}.")

                self.reminders.remove(doc_ids=to_remove)

            await asyncio.sleep(5)


def setup(bot):
    if logger.level == 0:  # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename='logs/reminders.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    bot.add_cog(Reminder(bot))
