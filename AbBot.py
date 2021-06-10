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

bot = commands.Bot(command_prefix="<", case_insensitive=True, owner_id=int(ADMIN_ID))

extensionList = [
                'cogs.Listeners',
                'cogs.Owner',
                'cogs.BotCommands'
                ]

async def status_change(): # randomizes statuses every hour (and also on startup :> )
    choice = random.randint(1, 3) # roll 1d3 nerd
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

bot.run(TOKEN)
