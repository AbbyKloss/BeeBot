import discord
from discord.ext import commands
from discord.ext import tasks
import time
import datetime
from datetime import timezone
import sqlite3



class Autosend(commands.Cog, description="opt in/out of things"): # TODO: rewrite this with database in mind  (6/12/2022 thought: is this not already done?)
    def __init__(self, bot):
        self.bot = bot
        self.thursday_loop.start()
        self.fgo_reminder_loop.start()
        self.meme_checker.start()

    async def get_memes_channels(self):
        con = sqlite3.connect('files/AbBotDatabase.db')
        cur = con.cursor()
        for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    cur.execute("select exists(select * from Channels where ChannelID=?)", (int(channel.id), ))
                    if ("meme" in channel.name) and (not cur.fetchone()[0]):
                        cur.execute("insert into Channels values (?, ?, 0, 1)", (int(channel.id), int(guild.id)))
                        con.commit()
        con.close()

    async def finally_thursday(self):
        con = sqlite3.connect('files/AbBotDatabase.db')
        cur = con.cursor()
        for row in cur.execute("select ChannelID from Channels where AutoBool=1"):
            channel = self.bot.get_channel(int(row[0]))
            try:
                await channel.send(content="https://cdn.discordapp.com/attachments/710704410329743390/865314343138361354/Its_Wednesday_or_as_I_like_to_call_it.mp4")
            except discord.errors.Forbidden:
                print("unallowed to enter " + str(channel.name) + "; " + str(row[0]))
        con.close()

    async def fgo_login_reminder(self):
        con = sqlite3.connect('files/AbBotDatabase.db')
        cur = con.cursor()
        for row in cur.execute("select ChannelID from Channels where FGOBool=1"):
            channel = self.bot.get_channel(int(row[0]))
            try:
                await channel.send(content="daily reminder to log into fgo :>")
            except discord.errors.Forbidden:
                print("unallowed to enter " + str(channel.name) + "; " + str(row[0]))
        con.close()

    async def fgo_timeup(self):
        utc_time = datetime.datetime.now(timezone.utc)
        minuteForm = ((int(utc_time.hour)*60) + (int(utc_time.minute))) # utc_time but just the hours and minutes in minute form
        if (utc_time.hour >= 4):
            timeuntil = 1680
        else:
            timeuntil = 240
        hours = int((timeuntil - minuteForm)/60)
        minutes = int((timeuntil - minuteForm) - hours*60)
        return str(hours) + " hours, " + str(minutes) + " minutes left until the daily reset :>"

    @tasks.loop(minutes=1.0) # made to check every minute if it's the top of the hour
    async def thursday_loop(self): # if so, then it'll send something
        #print("thursday_loop at: " + time.strftime("%H:%M:%S", time.localtime()))
        if ((datetime.datetime.today().weekday() == 3) and (datetime.datetime.now().hour == 12) and (datetime.datetime.now().minute == 0)): # should send on thursdays around noon
            await self.finally_thursday()
        elif (datetime.datetime.now().minute == 0):
            print("thursday loop hour marker: "+ time.strftime("%H:%M:%S", time.localtime()))
        #else:
            #print("not thursday...")

    @tasks.loop(minutes=1.0) # at the top of every hour that isn't 23:00, it prints it checked in the terminal
    async def fgo_reminder_loop(self): # if it _is_ 23:00, it sends something to the opt-in-ed channels
        #print ("fgo loop at: " + time.strftime("%H:%M:%S", time.localtime()))
        if ((datetime.datetime.now(timezone.utc).hour == 4) & (datetime.datetime.now(timezone.utc).minute == 0)):
            await self.fgo_login_reminder()
        elif (datetime.datetime.now().minute == 0):
            print("fgo loop hour marker: "+ time.strftime("%H:%M:%S", time.localtime()))
        #else:
            #print(await self.fgo_timeup())

    @tasks.loop(hours=24.0)
    async def meme_checker(self):
        print("daily meme channel check: " + time.strftime("%H:%M:%S", time.localtime()))
        await self.get_memes_channels()

    @commands.command(name='optOut', help='opts the current channel out of Autosend', usage='<optout') #this is a mess, comments here are mostly for me
    async def optOut(self, ctx):
        string = ""
        con = sqlite3.connect('files/AbBotDatabase.db')
        cur = con.cursor()
        cur.execute("select exists(select * from Channels where ChannelID=?)", (int(ctx.message.channel.id),))
        if (not cur.fetchone()[0]):
            string = "This channel already doesn't get Autosend"
        else:
            cur.execute("update Channels set AutoBool=0 where ChannelID=?", (int(ctx.message.channel.id),))
            cur.execute("delete from Channels where FGOBool=0 and AutoBool=0")
            string = "done! no more Autosend for this channel :>"
        con.commit()
        con.close()
        await ctx.reply(string, mention_author=False)

    @commands.command(name='optIn', help='opts the current channel into Autosend', usage='<optin')
    async def optIn(self, ctx):
        con = sqlite3.connect('files/AbBotDatabase.db')
        cur = con.cursor()
        cur.execute("select exists(select * from Channels where ChannelID=?)", (int(ctx.message.channel.id),))
        if (not cur.fetchone()[0]):
            cur.execute("insert into Channels values (?, ?, 0, 1)", (int(ctx.message.channel.id), int(ctx.guild.id)))
        else:
            cur.execute("update Channels set AutoBool=1 where ChannelID=?", (int(ctx.message.channel.id),))
        con.commit()
        con.close()
        await ctx.reply("done! Autosend turned on for this channel! :>", mention_author=False)

    @commands.command(name='fgoOptIn', help='sets a reminder to log into fgo!', usage='<fgooptin')
    async def fgoOptIn(self, ctx):
        con = sqlite3.connect('files/AbBotDatabase.db')
        cur = con.cursor()
        cur.execute("select exists(select * from Channels where ChannelID=?)", (int(ctx.message.channel.id),))
        if (not cur.fetchone()[0]):
            cur.execute("insert into Channels values (?, ?, 1, 0)", (int(ctx.message.channel.id), int(ctx.guild.id)))
        else:
            cur.execute("update Channels set FGOBool=1 where ChannelID=?", (int(ctx.message.channel.id),))
        con.commit()
        con.close()
        await ctx.reply("done! reminder set! :>", mention_author=False)

    @commands.command(name='fgoOptOut', help='removes the fgo login reminder', usage='<fgooptout')
    async def fgoOptOut(self, ctx):
        string = ""
        con = sqlite3.connect('files/AbBotDatabase.db')
        cur = con.cursor()
        cur.execute("select exists(select * from Channels where ChannelID=?)", (int(ctx.message.channel.id),))
        if (not cur.fetchone()[0]):
            string = "This channel already doesn't get fgo reminders"
        else:
            cur.execute("update Channels set FGOBool=0 where ChannelID=?", (int(ctx.message.channel.id),))
            cur.execute("delete from Channels where FGOBool=0 and AutoBool=0")
            string = "done! no more fgo reminders!"
        con.commit()
        con.close()
        await ctx.reply(string, mention_author=False)

    @commands.command(name='fgoTimeUp', help='time until the daily fgo reset', usage='<fgotimeup')
    async def fgoTimeUp(self, ctx):
        string = await self.fgo_timeup()
        await ctx.reply(string, mention_author=False)
        
def setup(bot):
    bot.add_cog(Autosend(bot))