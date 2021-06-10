import discord
from discord.ext import commands
import random

heartsList = [":heart:",":orange_heart:",":yellow_heart:",":green_heart:",":blue_heart:",":purple_heart:",":brown_heart:",":white_heart:",":cupid:",":gift_heart:",":sparkling_heart:",":heartpulse:",":heartbeat:",":revolving_hearts:",":two_hearts:",":heart_exclamation:",":heart_decoration:"] #there's a finite amount of heart emojis, i don't need a separate file for them
helloFile = open("files/helloList.txt", "r") #opens a file to let you have as many or as few greetings as you'd like. allows for modularity in the bot without having to restart it every time you wanna add a greeting
helloList = helloFile.read().splitlines()
helloFile.close()

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hi', help="henlo :>") # says hello :>
    async def hello(self, ctx, *args):
        if args != ():
            response = f'**{ctx.author.name}** said ' + random.choice(helloList) + ' to **'+ '{}'.format(' '.join(args)) + '**'
        else:
            response = random.choice(helloList) + f' **{ctx.author.name}**'
        await ctx.send(response)

    @commands.command(name='f', help="pays respects") # press f to pay respects
    async def ffunc(self, ctx, *args):
        if args != ():
            response = f'**{ctx.author.name}** has paid their respects for **'+ '{}'.format(' '.join(args)) + "** " + random.choice(heartsList)
        else:
            response = f'**{ctx.author.name}** has paid their respects ' + random.choice(heartsList)
        await ctx.send(response)

    @commands.command(name='3', help="<3") # does a heart emoji from heartsList
    async def heart(self, ctx):
        await ctx.send(random.choice(heartsList))

    @commands.command(name='invite', help='sends invite link :>') # self explanatory
    async def invite(self, ctx):
        await ctx.send("i heard you wanted to add me to your server! here's the link " + random.choice(heartsList) + "\nhttps://discord.com/oauth2/authorize?client_id=748302551933517835&permissions=8&scope=bot")

    @commands.command(name='github', help='github? dont know what that is :>')
    async def github(self, ctx):
        await ctx.send("i was told to give you a link so here you go! " + random.choice(heartsList) + "\nhttps://github.com/blampf/AbBot")

    @commands.command(name='google', help='google search!!') # kind of disgustingly rudimentary, it just returns a link of the first thing it finds
    async def websearch(self, ctx, *args):
        if args != "":
            query = '{}'.format(' '.join(args))
            for output in search(query, tld="com", num=1, stop=1, pause=1.0):
                await ctx.send(output)
        else:
            await ctx.send("i can't search for nothing,,")

def setup(bot):
    bot.add_cog(BotCommands(bot))
