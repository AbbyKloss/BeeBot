# AbBot.py
# Author: Abby Kloss
# TW: @heykloss

'''
Literally just a framework, everything happens in the cogs at this point
'''

import os
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch
from pretty_help import PrettyHelp, DefaultMenu

load_dotenv() # make sure you have all the things below filled out in your .env file
TOKEN    = os.getenv('DISCORD_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

def get_prefix(bot, message):
    prefixes = ""
    con = sqlite3.connect('files/AbBotDatabase.db')
    for row in con.cursor().execute("SELECT Prefix from Guilds where GuildID=?", (int(message.guild.id),)):
        prefixes = row[0]
    con.close()
    return prefixes

bot = commands.Bot(command_prefix=(get_prefix), case_insensitive=True, owner_id=int(ADMIN_ID))

# PrettyHelp block, for readability
endingnote = "note: [parameters] are optional, <parameters> are not"
menu = DefaultMenu('◀️', '▶️', '❌')
bot.help_command = PrettyHelp(navigation=menu, color=0xf5a9b8, ending_note=endingnote) 

# letting dotenv work across the bot
bot.GOOGLE_ID = str(os.getenv('GOOGLE_ID'))
bot.GOOGLE_CX = str(os.getenv('GOOGLE_CX'))
bot.GOOGLE_BU = str(os.getenv('GOOGLE_BU'))
bot.IMGUR_ID = os.getenv('IMGUR_ID')
bot.IMGUR_SECRET = os.getenv('IMGUR_SECRET')
bot.backupFlag = False # a way to get around the 100 queries/day, maybe don't do this, idk if im violating something here

bot.gis = GoogleImagesSearch(bot.GOOGLE_ID, bot.GOOGLE_CX) # i just ran out of test queries very quick because my code messed up

# things that hardly matter
bot.imageDesc = ""
bot.currentNSFW = False

# startup
extensionList = [
                'cogs.Listeners',
                'cogs.Owner',
                'cogs.BotCommands',
                'cogs.Autosend',
                'cogs.Info',
                'cogs.Images'
                ]

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guild(s):\n')
    for guild in bot.guilds:
        print(f'{guild.name} (id: {guild.id})')
    print(" ")
    for extension in extensionList:
        bot.load_extension(extension)

@bot.event
async def on_guild_join(guild):
    con = sqlite3.connect('files/AbBotDatabase.db')
    cur = con.cursor()
    cur.execute("insert into Guilds values (?, '<')", (int(guild.id), ))
    con.commit()
    con.close()

@bot.event
async def on_guild_remove(guild):
    con = sqlite3.connect('files/AbBotDatabase.db')
    cur = con.cursor()
    cur.execute("delete from Guilds where GuildID=?", (int(guild.id),))
    cur.execute("delete from Channels where GuildID=?", (int(guild.id),))
    con.commit()
    con.close()



bot.run(TOKEN)
