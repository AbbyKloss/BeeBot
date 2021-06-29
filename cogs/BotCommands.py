from discord.ext import commands
from googlesearch import search
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
            for output in search(query, tld="com", num=1, stop=1, pause=1.0): # API calls! fun! (it takes a fuckin while to actually get a reasult and sometimes you just don't get anything)
                await ctx.send(output)
        else:
            await ctx.send("i can't search for nothing,,")

    @commands.command(name='roll', help='rolls ndx! (add adv or dis afterwards to get (dis)advantage)')
    async def diceroll(self, ctx, arg="1d6", adv="no"): # defaults to the most basic of dice
        num = 1
        size = 0
        add = 0
        sum = 0
        maxnum = 0

        pos = arg.find('d')
        pluspos = arg.find('+')
        
        if pos == -1: # testing if it was input correctly (shhh idk how to make it to where incorrect things after that don't work, i need to look into exception handling)
            await ctx.send('please format your roll in the **n**d**x** system ' + random.choice(heartsList))
            return

        elif (pos == 0) and (pluspos == -1): # if the user just input 'd8' it should roll 1d8
            size = int(arg[pos+1:])
        elif (pos != 0) and (pluspos == -1):          # if it's input correctly, this will run
            num = int(arg[:pos])
            size = int(arg[pos+1:])
        else:
            num = int(arg[:pos])
            size = int(arg[pos+1:pluspos])
            add = int(arg[pluspos+1:])
        if (num > 300) or (size > 300):
            await ctx.send('too big........')
            return
        minnum = size
        sum += add
        if (size > 0) and (num > 0):
            message = f'**{ctx.author.name}** rolled: ' # setup 
            for i in range(num):
                randomroll = random.randint(1, size)
                maxnum = max(maxnum, randomroll)
                minnum = min(minnum, randomroll)
                sum += randomroll
                if randomroll == size:
                    randomroll = "***" + str(randomroll) + "***" # nice flavor, it italicizes and bolds a max roll
                elif randomroll == 1:
                    randomroll = "**" + str(randomroll) + "**" # bolds a min roll
                if (i+1 != num) and (num != 1):
                    message += str(randomroll) + ", " # appends the roll to the message that'll be sent
                else:
                    message += str(randomroll) # no extra commas, please
            if (pluspos != -1):
                message += ' (+' + str(add) + ')'
            message +='\nSum: ' + str(sum)
            if adv[0] == "a":
                message += '\nADV: ' + str(maxnum)
            elif adv[0] == "d":
                message += '\nDIS: ' + str(minnum)
            await ctx.send(message)
        else:
            await ctx.send("You Rolled.")


def setup(bot):
    bot.add_cog(BotCommands(bot))
