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

load_dotenv() # make sure you have all the things below filled out in your .env file
TOKEN    = os.getenv('DISCORD_TOKEN')
GUILD    = os.getenv('DISCORD_GUILD')
ADMIN_ID = os.getenv('ADMIN_ID')

# randomize statuses so it doesn't feel so static
gameStatuses = ["with your heart💙", "critically acclaimed mmorpg final fantasy fourt teen", "fin fant " + str(random.randrange(1, 15)), "monstie huntie", "lelda of zelda breath of the weath"]
musicStatuses = ["number 1 victory royale yeah fortnite we boutta get down (get down) 10 kills on the board right now just wiped out tomato town", "spoofy", "music on the you tubes", "tidal (i love jay z)", "More Dunkey More Problems"]
videoStatuses = ["idk some ding dong video on the you tube", "demons layer ;>", "vine land saga", "zombie vine land saga"]

heartsList = [":heart:",":orange_heart:",":yellow_heart:",":green_heart:",":blue_heart:",":purple_heart:",":brown_heart:",":white_heart:",":cupid:",":gift_heart:",":sparkling_heart:",":heartpulse:",":heartbeat:",":revolving_hearts:",":two_hearts:",":heart_exclamation:",":heart_decoration:"] #there's a finite amount of heart emojis, i don't need a separate file for them
helloFile = open("files/helloList.txt", "r") #opens a file to let you have as many or as few greetings as you'd like. allows for modularity in the bot without having to restart it every time you wanna add a greeting
helloList = helloFile.read().splitlines()
helloFile.close()
bot = commands.Bot(command_prefix="<", case_insensitive=True)

async def status_change(): # randomizes statuses every hour (and also on startup :> )
    choice = random.randrange(1, 3) # roll 1d3 nerd
    if choice == 1:   # playing
        await bot.change_presence(activity=discord.Game(random.choice(gameStatuses)))
    elif choice == 2: # listening
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(musicStatuses)))
    elif choice == 3: # watching
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(videoStatuses)))

async def startup(): # woo startup! so you know it uhh works!
    print(f'{bot.user} is connected to the following guild(s):\n')
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
        print(f'{guild.name} (id: {guild.id})')
    await status_change()

@bot.event
async def on_ready():
    await startup()

@tasks.loop(hours=1)
async def the_loop():
    await status_change()

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

@bot.command(name='github', help='github? dont know what that is :>')
async def github(ctx):
    await ctx.send("i was told to give you a link so here you go! " + random.choice(heartsList) + "\nhttps://github.com/blampf/AbBot")

@bot.command(name='google', help='google search!!') # kind of disgustingly rudimentary, it just returns a link of the first thing it finds
async def websearch(ctx, *args):
    if args != ():
        query = '{}'.format(' '.join(args))
        for output in search(query, tld="com", num=1, stop=1, pause=1.0):
            await ctx.send(output)
    else:
        await ctx.send("i can't search for nothing,,")

@bot.listen()
async def on_message(message):
    if "cope" in message.content.lower():
        emoji = '<:COPE:848006983726530601>'
        await message.add_reaction(emoji)

@bot.listen()
async def on_message(message):
    if "hope" in message.content.lower():
        emoji = '<:HOPE:848007900517629973>'
        await message.add_reaction(emoji)

@bot.listen()
async def on_message(message):
    if ("turtle" in message.content.lower()) or ("turble" in message.content.lower()) or ("tortle" in message.content.lower()) or ("🐢" in message.content.lower() or ("turdle" in message.content.lower())):
        emoji = '<:turble:848677634577006643>'
        await message.add_reaction(emoji)

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
            await ctx.send("`Access Denied.`")

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
            await ctx.send("`Access Denied.`")

@bot.command(name='changeStatus', hidden=True)
async def changeStatus(ctx):
    if str(ctx.author.id) == str(ADMIN_ID):
        await status_change()
        await ctx.send("done!")
    else:
        await ctx.send("`Access Denied.`")

bot.run(TOKEN)
