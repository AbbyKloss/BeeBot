import discord
from discord.ext import commands
from discord.ext import tasks
import time
import datetime

optOutFile = open("files/optOutList.txt", "r")
optOutList = optOutFile.read().splitlines()
optOutFile.close()
optInFile = open("files/optInList.txt", "r")
optInList = optInFile.read().splitlines()
optOutFile.close()
channelList = optInList.copy()

class Autosend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    if ("memes" in channel.name) and (str(channel.id) not in optOutList) and (str(channel.id) not in channelList):
                        channelList.append(channel.id)
                        #print(channelList)
        self.thursday_loop.start()

    """async def get_memes_channels(self):
        for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    if ("memes" in channel.name) and not (channel.name in optOutList):
                        channelList.append(channel.id)
                        print(channelList)"""

    @tasks.loop(hours=1)
    async def thursday_loop(self):
        #await get_memes_channels()
        print("thursday_loop at: " + time.strftime("%H:%M:%S", time.localtime()))
        if (datetime.datetime.today().weekday() == 3) and (datetime.datetime.now().hour == 12):
            print(channelList)
            for channelItem in channelList:
                channel = self.bot.get_channel(int(channelItem))
                try:
                    await channel.send(content="https://cdn.discordapp.com/attachments/710704410329743390/865314343138361354/Its_Wednesday_or_as_I_like_to_call_it.mp4")
                except discord.errors.Forbidden:
                    print("unallowed to enter " + str(channel.name))

    @commands.command(name='optOut', help='opts the current channel out of Autosend') #this is a mess, comments here are mostly for me
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
            await ctx.send("done! this channel won't be getting anything from Autosend anymore!")
        else:
            await ctx.send("this channel already doesn't get anything from Autosend..")

    @commands.command(name='optIn', help='opts the current channel into Autosend')
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
            await ctx.send("done! now this channel will get messages from Autosend :>")
        else:
            await ctx.send("you're already good to go!!")



def setup(bot):
    bot.add_cog(Autosend(bot))