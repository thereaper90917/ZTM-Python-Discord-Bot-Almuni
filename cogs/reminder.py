import discord
from discord.ext import commands
import os
import asyncio
import time
import logging
from tinydb import Query, TinyDB


class Reminder(commands.Cog):
    """Never forget anything anymore."""

    def __init__(self, bot):
        self.bot = bot
        self.reminders = TinyDB('data/reminders.db')
        self.units = {"minute": 60, "hour": 3600, "day": 86400, "week": 604800, "month": 2592000}

    @commands.command(pass_context=True)
    async def reminder(self, ctx, quantity: int, time_unit: str, *, text: str):
        """Sends you <text> when the time is up
        Accepts: minutes, hours, days, weeks, month
        Example:
        [p]reminder 3 days Have sushi with Asu and JennJenn"""
        time_unit = time_unit.lower()
        author = ctx.message.author
        s = ""
        if time_unit.endswith("s"):
            time_unit = time_unit[:-1]
            s = "s"
        if time_unit not in self.units:
            await ctx.send("Invalid time unit. Choose minutes/hours/days/weeks/month")
            return
        if quantity < 1:
            await ctx.send("Quantity must not be 0 or negative.")
            return
        if len(text) > 1960:
            await ctx.send("Text is too long.")
            return
        seconds = self.units[time_unit] * quantity
        future = int(time.time() + seconds)
        data = {"id": author.id,
                "remind_at": future,
                "message": text}
        self.reminders.insert(data)
        logger.info("{} ({}) set a reminder.".format(author.name, author.id))
        await ctx.send("I will remind you of that in {} {}.".format(str(quantity), time_unit + s))

    @commands.command(pass_context=True)
    async def forget_reminder(self, ctx):
        """Removes all your upcoming notifications"""
        author = ctx.message.author
        to_remove = []
        for reminder in self.reminders:
            if reminder["id"] == author.id:
                to_remove.append(reminder)

        if not to_remove == []:
            for reminder in to_remove:
                self.reminders.remove(reminder)
            await self.bot.say("All your notifications have been removed.")
        else:
            await self.bot.say("You don't have any upcoming notification.")

    async def check_reminders(self):
        while self is self.bot.get_cog("Reminder"):
            to_remove = []
            for reminder in self.reminders:
                if reminder["remind_at"] <= int(time.time()):
                    try:
                        await self.bot.send_message(discord.User(id=reminder["id"]),
                                           "You asked me to remind you this:\n{}".format(reminder["message"]))
                    except (discord.errors.Forbidden, discord.errors.NotFound):
                        to_remove.append(reminder)
                    except discord.errors.HTTPException:
                        pass
                    else:
                        to_remove.append(reminder)
            for reminder in to_remove:
                self.reminders.remove(reminder)
            await asyncio.sleep(5)


def setup(bot):
    global logger
    logger = logging.getLogger("reminders")
    if logger.level == 0:  # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='logs/reminders.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    n = Reminder(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n.check_reminders())
    bot.add_cog(n)
