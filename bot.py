# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

import discord
from discord.ext import commands

heartsList = [":heart:",":orange_heart:",":yellow_heart:",":green_heart:",":blue_heart:",":purple_heart:",":brown_heart:",":white_heart:",":cupid:",":gift_heart:",":sparkling_heart:",":heartpulse:",":heartbeat:",":revolving_hearts:",":two_hearts:",":heart_exclamation:",":heart_decoration:"]
helloList = ["henlo", "howdy", "hi", "meowdy", "nyello", "heblo", "yello", "hiiiiii", "hi hi", "konnichiwa"]
bot = commands.Bot(command_prefix="<", case_insensitive=True)

print("ready")

@bot.command(name='hi', help="henlo :>")
async def hello(ctx, *args):
    #person = f"{ctx.author.name}"
    randomHi = random.randrange(len(helloList))
    if args != ():
        response = "**" + f"{ctx.author.name}** said " + helloList[randomHi] + " to **"+ '{}'.format(' '.join(args)) + "** "
    else:
        response = helloList[randomHi] + " **" + f"{ctx.author.name}" + "**"
    await ctx.send(response)

@bot.command(name='f', help="pays respects")
async def ffunc(ctx, *args):
    randomHeart = random.randrange(len(heartsList))
    if args != ():
        response = "**" + f"{ctx.author.name}** has paid their respects for **"+ '{}'.format(' '.join(args)) + "** " + heartsList[randomHeart]
    else:
        response = "**" + f"{ctx.author.name}** has paid their respects " + heartsList[randomHeart]
    await ctx.send(response)

@bot.command(name='3', help="<3")
async def ffunc(ctx):
    randomNumber = random.randrange(16)
    await ctx.send(heartsList[randomNumber])

bot.run(TOKEN)
