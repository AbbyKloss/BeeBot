# AbBot.py
# Author: Abby Kloss
# TW: @heykloss
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

load_dotenv() # make sure you have all the things below filled out in your .env file
TOKEN    = os.getenv('DISCORD_TOKEN')
GUILD    = os.getenv('DISCORD_GUILD')
ADMIN_ID = os.getenv('ADMIN_ID')

import discord
from discord.ext import commands

heartsList = [":heart:",":orange_heart:",":yellow_heart:",":green_heart:",":blue_heart:",":purple_heart:",":brown_heart:",":white_heart:",":cupid:",":gift_heart:",":sparkling_heart:",":heartpulse:",":heartbeat:",":revolving_hearts:",":two_hearts:",":heart_exclamation:",":heart_decoration:"] #there's a finite amount of heart emojis, i don't need a separate file for them
helloFile = open("files/helloList.txt", "r") #opens a file to let you have as many or as few greetings as you'd like. allows for modularity in the bot without having to restart it every time you wanna add a greeting
helloList = helloFile.read().splitlines()
helloFile.close()
bot = commands.Bot(command_prefix="<", case_insensitive=True, activity=discord.Game('with your heart💙'))

print("AbBot is online.") # this line states that you're just ready to zoom, the bot is running


@bot.command(name='hi', help="henlo :>") # says hello :>
async def hello(ctx, *args):
    if args != ():
        response = "**" + f"{ctx.author.name}** said " + random.choice(helloList) + " to **"+ '{}'.format(' '.join(args)) + "**"
    else:
        response = random.choice(helloList) + " **" + f"{ctx.author.name}" + "**"
    await ctx.send(response)

@bot.command(name='f', help="pays respects") # press f to pay respects
async def ffunc(ctx, *args):
    if args != ():
        response = "**" + f"{ctx.author.name}** has paid their respects for **"+ '{}'.format(' '.join(args)) + "** " + random.choice(heartsList)
    else:
        response = "**" + f"{ctx.author.name}** has paid their respects " + random.choice(heartsList)
    await ctx.send(response)

@bot.command(name='3', help="<3") # does a heart emoji from heartsList
async def heart(ctx):
    await ctx.send(random.choice(heartsList))

@bot.command(name='invite', help='sends invite link :>') # self explanatory
async def invite(ctx):
    await ctx.send("i heard you wanted to add me to your server! here's the link " + random.choice(heartsList) + "\nhttps://discord.com/oauth2/authorize?client_id=748302551933517835&permissions=8&scope=bot")

@bot.command(name='addHi', hidden=True) # adds a greeting to files/helloList.txt
async def addHi(ctx, *args):            # if you're not me and you're running a copy of this, add your userID to the .env file
    if args != ():                      # i did "$dotenv set ADMIN_ID [userID]"
        if str(ctx.author.id) == str(ADMIN_ID): # this is sloppy but it didn't work without typecasting for whatever reason. it works if it's not in the .env, but im not keeping my userID out in the open
            newGreeting = '{}'.format(' '.join(args))
            if not (newGreeting in helloList):
                helloFile = open("files/helloList.txt", "a")
                helloFile.write(newGreeting + '\n')
                helloList.append(newGreeting)
                helloFile.seek(0)
                print(helloList) # debug code to make sure it all works properly
                helloFile.close()
                await ctx.send("**" + newGreeting + "** added to `helloList.txt`!")
            else:
                await ctx.send("**" + newGreeting + "** already in `helloList.txt`")
        else:
            await ctx.send("```Access Denied.```")

@bot.command(name='removeHi', hidden=True) # in case i somehow get a bad greeting in there >:< (angy)
async def removeHi(ctx, *args):
    if args != ():
        if str(ctx.author.id) == str(ADMIN_ID):
            badGreeting = '{}'.format(' '.join(args))
            if badGreeting in helloList:
                helloList.remove(badGreeting)
                helloFile = open("files/helloList.txt", "w")
                for greeting in helloList: # im sure there's a better way of fixing the list than this, but this is what i got right now. it sucks the larger the list gets
                    helloFile.write(greeting + '\n')
                helloFile.close()
                print(helloList)
                await ctx.send("done! you won't see **" + badGreeting + "** in there anymore!")
            else:
                await ctx.send("im not seeing **" + badGreeting + "** in the list,,")
        else:
            await ctx.send("```Access Denied.```")


bot.run(TOKEN)
