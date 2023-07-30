import datetime
from datetime import timezone
import json
import time

import discord
from discord.ext import commands
from discord.ext import tasks
import sqlite3


linksPath = "files/autosendLinks.json" # <- path to the json we want for our funny links

# TODO: rewrite this with database in mind  (6/12/2022 thought: is this not already done?)
# (3/26/2023 note: this has been done forever, a json would be better though.
#   the database decisions i made a year+ ago have debilitating side effects 
#   and i would like to unmake those decisions, but i don't have the time)
class Autosend(commands.Cog, description="opt in/out of things"):
  def __init__(self, bot):
    self.bot = bot

    # # testing it
    # s = schedule.every(5).seconds.do(self.test_wrapper, "test words")
    # # print(s.next_)run

    # # FGO Login Reminder
    # schedule.every().day.at("23:00", ptz('UTC')).do(self.fgo_wrapper)

    # # Gandalf Monday
    # monday_link = "https://www.youtube.com/watch?v=Dhz3uos4hpU"
    # schedule.every().monday.at("12:00").do(self.send_daily_link, monday_link)

    # # Out of Touch ~~thursdays~~ tuesdays
    # tuesday_link = "https://cdn.discordapp.com/attachments/826317763127017504/1089739891946029157/out_of_touch_tuesdays.mp4"
    # schedule.every().tuesday.at("12:00").do(self.send_daily_link, "out of touch ~~thursday~~ tuesday!!!")
    # schedule.every().tuesday.at("12:00").do(self.send_daily_link, tuesday_link)

    # # Jerma Wednesday
    # wednesday_link = "https://media.tenor.com/akyBQEG1F5MAAAAC/sparkle-on-its-wednesday-dont-forget-to-be-yourself.gif"
    # schedule.every().wednesday.at("12:00").do(self.send_daily_link, wednesday_link)

    # # Feliz Hueves
    # thursday_link = "https://cdn.discordapp.com/attachments/710704410329743390/865314343138361354/Its_Wednesday_or_as_I_like_to_call_it.mp4"
    # schedule.every().thursday.at("12:00").do(self.send_daily_link, thursday_link)

    # # flat fuck friday
    # friday_link = "https://cdn.discordapp.com/attachments/826317763127017504/1089741205929201814/flat_fuck_friday.mp4"
    # schedule.every().friday.at("12:00").do(self.send_daily_link, friday_link)


    # something else
    # schedule.every().day.at("23:00", ptz('UTC')).do(self.fgo_login_reminder())

    # checking meme channels, doesn't need the precision of the new library
    self.meme_checker.start()

    # FGO Login Reminder
    self.fgo_reminder_loop.start()

    # Weekday memes
    self.weekday_loop.start()

    # while True:
    #   schedule.run_pending()
    #   time.sleep(1)

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

  # def test_wrapper(self, words):
  #   await tester(words)

  # async def tester(self, words):
  #   print(words)
  #   channel =self.bot.get_channel(865329749060222986)
  #   await channel.send(content=words)

  async def send_daily_link(self, link):
    print("Daily link now")
    con = sqlite3.connect('files/AbBotDatabase.db')
    cur = con.cursor()
    for row in cur.execute("select ChannelID from Channels where AutoBool=1"):
      channel = self.bot.get_channel(int(row[0]))
      try:
        await channel.send(content=link)
      except discord.errors.Forbidden:
        print("unallowed to enter " + str(channel.name) + "; " + str(row[0]))
    con.close()

  # def fgo_wrapper(self):
  #   await fgo_login_reminder()

  async def fgo_login_reminder(self):
    print("login reminder happening")
    con = sqlite3.connect('files/AbBotDatabase.db')
    cur = con.cursor()
    for row in cur.execute("select ChannelID from Channels where FGOBool=1"):
      channel = self.bot.get_channel(int(row[0]))
      try:
        await channel.send(content="daily reminder to log into fgo :>")
      except discord.errors.Forbidden:
        print("unallowed to enter " + str(channel.name) + "; " + str(row[0]))
    con.close()

  # async def fgo_timeup(self):
  #     utc_time = datetime.datetime.now(timezone.utc)
  #     minuteForm = ((int(utc_time.hour)*60) + (int(utc_time.minute))) # utc_time but just the hours and minutes in minute form
  #     if (utc_time.hour >= 4):
  #         timeuntil = 1680
  #     else:
  #         timeuntil = 240
  #     hours = int((timeuntil - minuteForm)/60)
  #     minutes = int((timeuntil - minuteForm) - hours*60)
  #     return str(hours) + " hours, " + str(minutes) + " minutes left until the daily reset :>"

  @tasks.loop(minutes=1.0) # made to check every minute if it's the top of the hour
  async def weekday_loop(self, debug=False, ctx=None): # if so, then it'll send something
    #print("thursday_loop at: " + time.strftime("%H:%M:%S", time.localtime()))
    print(f"testing thursday | {time.strftime('%H:%M:%S', time.localtime())}")
    if (not debug) and (not ((datetime.datetime.now().hour == 12) and (datetime.datetime.now().minute == 0))): # checking if noon
      return

    with open(linksPath, "r") as infile:
      data = json.load(infile)
      iter = data["iter"] % len(data[str(datetime.datetime.today().weekday())])
      link = data[str(datetime.datetime.today().weekday())][iter]
      
      



    # # mondays
    # if (datetime.datetime.today().weekday() == 0):
    #   link = "https://www.youtube.com/watch?v=Dhz3uos4hpU"

    # elif (datetime.datetime.today().weekday() == 1):
    #   # tuesdays 
    #   link = "https://cdn.discordapp.com/attachments/826317763127017504/1089739891946029157/out_of_touch_tuesdays.mp4"

    # # wednesdays
    # elif (datetime.datetime.today().weekday() == 2):
    #   link = "https://media.tenor.com/akyBQEG1F5MAAAAC/sparkle-on-its-wednesday-dont-forget-to-be-yourself.gif"

    # # thursdays
    # elif (datetime.datetime.today().weekday() == 3):
    #   link = "https://cdn.discordapp.com/attachments/710704410329743390/865314343138361354/Its_Wednesday_or_as_I_like_to_call_it.mp4"

    # # fridays
    # elif (datetime.datetime.today().weekday() == 4):
    #   link = "https://cdn.discordapp.com/attachments/826317763127017504/1089741205929201814/flat_fuck_friday.mp4"

    # elif (datetime.datetime.now().minute == 0):
    #     print("weekday loop hour marker: "+ time.strftime("%H:%M:%S", time.localtime()))

    # messing with the iterator value
    if datetime.datetime.today().weekday() == 6:
      iter = data["iter"] + 1
      maxes = [len(data[item]) for item in data.keys()]

      if iter > 100 + max(maxes): # arbitrary value, basically you will ideally not notice it? this isn't exactly designed, just kinda thrown together
        iter = 0                  # i hope that much is obvious from the many many commented out lines and the general mess of the place
                                  # i get paid to do this job better at an office

      data["iter"] = iter
      with open(linksPath, "w") as outfile:
        json.dump(data, outfile, indent=2)
    
    if link != "":
      if debug and (ctx is not None):
        print(link)
        await ctx.reply(link, mention_author=False)
        return
      await self.send_daily_link(link)
      

  @tasks.loop(minutes=1.0) # at the top of every hour that isn't 23:00, it prints it checked in the terminal
  async def fgo_reminder_loop(self): # if it _is_ 23:00, it sends something to the opt-in-ed channels
      print(f"testing fgo | {time.strftime('%H:%M:%S', time.localtime())}")
      if ((datetime.datetime.now(timezone.utc).hour == 4) & (datetime.datetime.now(timezone.utc).minute == 0)):
          await self.fgo_login_reminder()
      elif (datetime.datetime.now().minute == 0):
          print("fgo loop hour marker: "+ time.strftime("%H:%M:%S", time.localtime()))

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
        
  @commands.command(name='sendCurrentDay', help='autosend for right gosh darned now', usage='<sendcurrentday')
  @commands.is_owner()
  async def sendCurrentDay(self, ctx):
    await self.weekday_loop(True, ctx)

def setup(bot):
  bot.add_cog(Autosend(bot))