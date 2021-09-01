# AbBot.py
# Author: Abby Kloss
# TW: @heykloss

'''
Literally just a framework, everything happens in the cogs at this point
'''

import os
from discord.ext import commands
from dotenv import load_dotenv
from imgurpython import ImgurClient
from google_images_search import GoogleImagesSearch

# you can provide API key and CX using arguments,
# or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX


load_dotenv() # make sure you have all the things below filled out in your .env file
TOKEN    = os.getenv('DISCORD_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
IMGUR_ID = os.getenv('IMGUR_ID')
IMGUR_SECRET = os.getenv('IMGUR_SECRET')

imgClient = ImgurClient(IMGUR_ID, IMGUR_SECRET)

bot = commands.Bot(command_prefix="<", case_insensitive=True, owner_id=int(ADMIN_ID))


bot.GOOGLE_ID = str(os.getenv('GOOGLE_ID'))
bot.GOOGLE_CX = str(os.getenv('GOOGLE_CX'))
bot.GOOGLE_BU = str(os.getenv('GOOGLE_BU'))
bot.backupFlag = False # a way to get around the 100 queries/day, maybe don't do this, idk if im violating something here
bot.gis = GoogleImagesSearch(bot.GOOGLE_ID, bot.GOOGLE_CX) # i just ran out of test queries very quick because my code messed up
bot.imgClient = imgClient
bot.currentNSFW = False

extensionList = [
                'cogs.Listeners',
                'cogs.Owner',
                'cogs.BotCommands',
                'cogs.Autosend'
                ]

@bot.event
async def on_ready(): # woo startup! so you know it uhh works!
    print(f'{bot.user} is connected to the following guild(s):\n')
    for guild in bot.guilds:
        print(f'{guild.name} (id: {guild.id})')
    print(" ")
    for extension in extensionList:
        bot.load_extension(extension)

bot.run(TOKEN)
