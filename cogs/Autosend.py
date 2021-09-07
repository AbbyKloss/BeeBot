import discord
from discord.ext import commands
from discord.ext import tasks
import time
import datetime
from datetime import timezone

optOutFile = open("files/optOutList.txt", "r")
optOutList = optOutFile.read().splitlines()
optOutFile.close()
optInFile = open("files/optInList.txt", "r")
optInList = optInFile.read().splitlines()
optOutFile.close()
channelList = optInList.copy()

fgoFile = open("files/fgoList.txt", "r")
fgoList = fgoFile.read().splitlines()
fgoFile.close()
fgoChannelList = fgoList.copy() # not currently sure i need this, i haven't planned very far ahead
#startMinute = datetime.datetime.now(timezone.utc).minute

class Autosend(commands.Cog, description="opt in/out of things"):
    def __init__(self, bot):
        self.bot = bot
        self.thursday_loop.start()
        self.fgo_reminder_loop.start()
        self.meme_checker.start()

    async def get_memes_channels(self):
        for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    if ("meme" in channel.name) and (str(channel.id) not in optOutList) and (str(channel.id) not in channelList):
                        channelList.append(channel.id)

    async def finally_thursday(self):
        for channelItem in channelList:
            channel = self.bot.get_channel(int(channelItem))
            try:
                await channel.send(content="https://cdn.discordapp.com/attachments/710704410329743390/865314343138361354/Its_Wednesday_or_as_I_like_to_call_it.mp4")
            except discord.errors.Forbidden:
                print("unallowed to enter " + str(channel.name) + "; " + str(channelItem))

    async def fgo_login_reminder(self):
        for channelItem in fgoList:
            channel = self.bot.get_channel(int(channelItem))
            try:
                await channel.send(content="daily reminder to log into fgo :>")
            except discord.errors.Forbidden:
                print("unallowed to enter " + str(channel.name) + "; " + str(channelItem))

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
            print(channelList)
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
        badChannel = str(ctx.message.channel.id)
        print(badChannel)
        if (badChannel in channelList): # checks if the bad channel is in the list of channels we want to send to
            channelList.remove(badChannel) #removes the bad channel from the current list of things so we don't have to like reload the cog
            if badChannel in optInList: #checks if it's in the opt in list, which is smaller than the channelList
                optInList.remove(badChannel)
            optInFile = open("files/optInList.txt", "w") #opens file so we can use it
            for item in optInList: # for each item in the opt in list, we write it to the optInFile so it's like, correct
                optInFile.write(item + '\n')
            optInFile.close() #close
            optOutList.append(badChannel) # puts the bad channel on the optoutlist so we don't send to it
            optOutFile = open("files/optOutList.txt", "w")
            for item in optOutList:
                optOutFile.write(item + '\n')
            optOutFile.close()
            print(optOutList)
            await ctx.reply("done! this channel won't be getting anything from Autosend anymore!", mention_author=False)
        else:
            await ctx.reply("this channel already doesn't get anything from Autosend..", mention_author=False)

    @commands.command(name='optIn', help='opts the current channel into Autosend', usage='<optin')
    async def optIn(self, ctx):
        goodChannel = str(ctx.message.channel.id)
        print(goodChannel)
        if not(goodChannel in channelList): # if it's in the channel list, then it's in the optin list or it gets added every time
            if goodChannel in optOutList: # checking if it's in the optout list so it doesn't get ignored every time anyways
                optOutList.remove(goodChannel)
                optOutFile = open("files/optOutList.txt", "w")
                for item in optOutList: #rewriting the optoutfile
                    optOutFile.write(item + '\n')
                optOutFile.close()
            channelList.append(goodChannel) # adding it to the appropriate lists
            optInList.append(goodChannel)
            optInFile = open("files/optInList.txt", "w")
            for item in optInList:
                optInFile.write(item + '\n')
            optInFile.close()
            print(channelList)
            await ctx.reply("done! now this channel will get messages from Autosend :>", mention_author=False)
        else:
            await ctx.reply("you're already good to go!!", mention_author=False)

    @commands.command(name='fgoOptIn', help='sets a reminder to log into fgo!', usage='<fgooptin')
    async def fgoOptIn(self, ctx):
        goodChannel = str(ctx.message.channel.id)
        if not(goodChannel in fgoChannelList):
            fgoChannelList.append(goodChannel)
            fgoList.append(goodChannel)
            fgoFile = open("files/fgoList.txt", "w")
            for item in fgoList:
                fgoFile.write(item + '\n')
            fgoFile.close()
            print(fgoChannelList)
            await ctx.reply("done! reminder set :>", mention_author=False)
        else:
            await ctx.reply("reminder's already set!", mention_author=False)

    @commands.command(name='fgoOptOut', help='removes the fgo login reminder', usage='<fgooptout')
    async def fgoOptOut(self, ctx):
        badChannel = str(ctx.message.channel.id)
        if (badChannel in fgoChannelList):
            fgoChannelList.remove(badChannel)
            fgoList.remove(badChannel)
            fgoFile = open("files/fgoList.txt", "w")
            for item in fgoList:
                fgoFile.write(item + '\n')
            fgoFile.close()
            print(fgoChannelList)
            await ctx.reply("alright! you won't get reminders anymore :>", mention_author=False)
        else:
            await ctx.reply("you already don't get reminders :/", mention_author=False)

    @commands.command(name='fgoTimeUp', help='time until the daily fgo reset', usage='<fgotimeup')
    async def fgoTimeUp(self, ctx):
        string = await self.fgo_timeup()
        await ctx.reply(string, mention_author=False)


def setup(bot):
    bot.add_cog(Autosend(bot))