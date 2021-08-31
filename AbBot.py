# AbBot.py
# Author: Abby Kloss
# TW: @heykloss

'''
Literally just a framework, everything happens in the cogs at this point
'''

import os
from discord.ext import commands
#from discord import Client, Intents, Embed
from dotenv import load_dotenv
#from discord_slash import SlashCommand, SlashContext


load_dotenv() # make sure you have all the things below filled out in your .env file
TOKEN    = os.getenv('DISCORD_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

bot = commands.Bot(command_prefix="<", case_insensitive=True, owner_id=int(ADMIN_ID))
#slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

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
