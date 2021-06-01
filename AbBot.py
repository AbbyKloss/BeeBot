# AbBot.py
# Author: Abby Kloss
# TW: @heykloss

import os
import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
from googlesearch import search
import random
import time


load_dotenv() # make sure you have all the things below filled out in your .env file
TOKEN    = os.getenv('DISCORD_TOKEN')
GUILD    = os.getenv('DISCORD_GUILD')
ADMIN_ID = os.getenv('ADMIN_ID')

# randomize statuses so it doesn't feel so static
gameStatuses = ["with your heart💙", "critically acclaimed mmorpg final fantasy fourt teen", "fin fant " + str(random.randrange(1, 15)), "monstie huntie", "lelda of zelda breath of the weath"]
musicStatuses = ["number 1 victory royale yeah fortnite we boutta get down (get down) 10 kills on the board right now just wiped out tomato town", "spoofy", "music on the you tubes", "tidal (i love jay z)", "More Dunkey More Problems"]
videoStatuses = ["idk some ding dong video on the you tube", "demons layer ;>", "vine land saga", "zombie vine land saga"]

heartsList = [":heart:",":orange_heart:",":yellow_heart:",":green_heart:",":blue_heart:",":purple_heart:",":brown_heart:",":white_heart:",":cupid:",":gift_heart:",":sparkling_heart:",":heartpulse:",":heartbeat:",":revolving_hearts:",":two_hearts:",":heart_exclamation:",":heart_decoration:"] #there's a finite amount of heart emojis, i don't need a separate file for them
bot = commands.Bot(command_prefix="<", case_insensitive=True, owner_id=int(ADMIN_ID))

extensionList = [
                'cogs.listeners',
                'cogs.owner',
                'cogs.botcommands'
                ]

async def status_change(): # randomizes statuses every hour (and also on startup :> )
    choice = random.randrange(1, 3) # roll 1d3 nerd
    if choice == 1:   # playing
        await bot.change_presence(activity=discord.Game(random.choice(gameStatuses)))
    elif choice == 2: # listening
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(musicStatuses)))
    elif choice == 3: # watching
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(videoStatuses)))

@bot.event
async def on_ready(): # woo startup! so you know it uhh works!
    print(f'{bot.user} is connected to the following guild(s):\n')
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
        print(f'{guild.name} (id: {guild.id})')
    print(" ")
    for extension in extensionList:
        bot.load_extension(extension)
    the_loop.start()

@tasks.loop(hours=1)
async def the_loop():
    print("automatically changed status at: " + time.strftime("%H:%M:%S", time.localtime())) # prints to the console so you know the status actually changed with a timestamp so you know when
    await status_change()

# @bot.command(name='hi', help="henlo :>") # says hello :>
# async def hello(ctx, *args):
#     if args != ():
#         response = "**" + f"{ctx.author.name}** said " + random.choice(helloList) + " to **"+ '{}'.format(' '.join(args)) + "**"
#     else:
#         response = random.choice(helloList) + " **" + f"{ctx.author.name}" + "**"
#     await ctx.send(response)
#
# @bot.command(name='f', help="pays respects") # press f to pay respects
# async def ffunc(ctx, *args):
#     if args != ():
#         response = "**" + f"{ctx.author.name}** has paid their respects for **"+ '{}'.format(' '.join(args)) + "** " + random.choice(heartsList)
#     else:
#         response = "**" + f"{ctx.author.name}** has paid their respects " + random.choice(heartsList)
#     await ctx.send(response)
#
# @bot.command(name='3', help="<3") # does a heart emoji from heartsList
# async def heart(ctx):
#     await ctx.send(random.choice(heartsList))
#
# @bot.command(name='invite', help='sends invite link :>') # self explanatory
# async def invite(ctx):
#     await ctx.send("i heard you wanted to add me to your server! here's the link " + random.choice(heartsList) + "\nhttps://discord.com/oauth2/authorize?client_id=748302551933517835&permissions=8&scope=bot")
#
# @bot.command(name='github', help='github? dont know what that is :>')
# async def github(ctx):
#     await ctx.send("i was told to give you a link so here you go! " + random.choice(heartsList) + "\nhttps://github.com/blampf/AbBot")
#
# @bot.command(name='google', help='google search!!') # kind of disgustingly rudimentary, it just returns a link of the first thing it finds
# async def websearch(ctx, *args):
#     if args != ():
#         query = '{}'.format(' '.join(args))
#         for output in search(query, tld="com", num=1, stop=1, pause=1.0):
#             await ctx.send(output)
#     else:
#         await ctx.send("i can't search for nothing,,")

bot.run(TOKEN)
