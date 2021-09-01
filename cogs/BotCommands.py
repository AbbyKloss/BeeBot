from discord.ext import commands
from googlesearch import search
from imgurpython import ImgurClient
from google_images_search import GoogleImagesSearch
from googleapiclient import errors as gerrors
from pathlib import Path
import discord
import random
import os

heartsList = [":heart:",":orange_heart:",":yellow_heart:",":green_heart:",":blue_heart:",":purple_heart:",":brown_heart:",":white_heart:",":cupid:",":gift_heart:",":sparkling_heart:",":heartpulse:",":heartbeat:",":revolving_hearts:",":two_hearts:",":heart_exclamation:",":heart_decoration:"] #there's a finite amount of heart emojis, i don't need a separate file for them
helloFile = open("files/helloList.txt", "r") #opens a file to let you have as many or as few greetings as you'd like. allows for modularity in the bot without having to restart it every time you wanna add a greeting
helloList = helloFile.read().splitlines()
helloFile.close()
albumList = list()

_search_params = { # for <imageSearch
    'q': '...',
    'num': 1,
    'safe': 'off',
    'fileType': 'jpg'
    #'imgType': 'clipart|face|lineart|news|photo',
    #'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge',
    #'imgDominantColor': 'black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow',
    #'imgColorType': 'color|gray|mono|trans',
    #'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
}

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #sebbyAlbum = bot.imgClient.get_album('dYPnFKD')

    @commands.command(name='hi', help="henlo :>") # says hello :>
    async def hello(self, ctx, *args):
        if args != ():
            response = f'**{ctx.author.name}** said ' + random.choice(helloList) + ' to **'+ '{}'.format(' '.join(args)) + '**'
        else:
            response = random.choice(helloList) + f' **{ctx.author.name}**'
        await ctx.reply(response, mention_author=False)

    @commands.command(name='f', help="pays respects") # press f to pay respects
    async def ffunc(self, ctx, *args):
        if args != ():
            response = f'**{ctx.author.name}** has paid their respects for **'+ '{}'.format(' '.join(args)) + "** " + random.choice(heartsList)
        else:
            response = f'**{ctx.author.name}** has paid their respects ' + random.choice(heartsList)
        await ctx.reply(response, mention_author=False)

    @commands.command(name='3', help="<3") # does a heart emoji from heartsList
    async def heart(self, ctx):
        await ctx.reply(random.choice(heartsList), mention_author=False)

    @commands.command(name='invite', help='sends invite link :>') # self explanatory
    async def invite(self, ctx):
        await ctx.reply("i heard you wanted to add me to your server! here's the link " + random.choice(heartsList) + "\nhttps://discord.com/oauth2/authorize?client_id=748302551933517835&permissions=2147798080&scope=bot", mention_author=False)

    @commands.command(name='github', help='github? dont know what that is :>')
    async def github(self, ctx):
        await ctx.reply("i was told to give you a link so here you go! " + random.choice(heartsList) + "\nhttps://github.com/blampf/AbBot", mention_author=False)

    @commands.command(name='google', help='google search!!') # kind of disgustingly rudimentary, it just returns a link of the first thing it finds
    async def websearch(self, ctx, *args):
        if args != "":
            query = '{}'.format(' '.join(args))
            for output in search(query, tld="com", num=1, stop=1, pause=1.0): # API calls! fun! (it takes a fuckin while to actually get a reasult and sometimes you just don't get anything)
                await ctx.reply(output, mention_author=False)
        else:
            await ctx.reply("i can't search for nothing,,", mention_author=False)

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
            await ctx.reply('too big........', mention_author=False)
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
            await ctx.reply(message, mention_author=False)
        else:
            await ctx.reply("You Rolled.", mention_author=False)

    @commands.command(name='notCat', help="cat pix", hidden=True)
    #@commands.is_nsfw()
    async def not_cat(self, ctx):
        if ctx.channel.is_nsfw(): 
            albumList.clear()
            for img in self.bot.imgClient.get_album_images('J3bm5gs'):
                    albumList.append(img.link)
            await ctx.reply(str(random.choice(albumList)), mention_author=False)
        else:
            await ctx.reply("currently an nsfw command ;>", mention_author=False)

    @commands.command(name='iSearch', help='google image search!')
    async def image_search(self, ctx, *args):
        if args != "":
            query = '{}'.format(' '.join(args)) # this and the above line are copied from the google search command
            _search_params['q'] = query         # modifying the dictionary
            if ctx.channel.is_nsfw(): 
                _search_params['safe'] = 'off'
                self.bot.currentNSFW = True
            else:
                _search_params['safe'] = 'medium'
                self.bot.currentNSFW = False
            error_message = ""
            filename = "currentImage.jpg"
            fp = "images/currentImage.jpg"
            file_path = Path("images/currentImage.jpg") # deleting current currentImage.jpg
            if file_path.is_file():
                try:
                    os.remove(file_path)
                except OSError as e:
                    filename = "currentImage(1).jpg"
                    fp = "images/currentImage(1).jpg"
                    print("Error: %s : %s" % (file_path, e.strerror))
            try:
                self.bot.gis.search(search_params=_search_params, path_to_dir="images/", custom_image_name='currentImage') # testing thingy

            except:# (commands.errors.CommandInvokeError or gerrors.HttpError): # something complicated to get around the 100 queries/day
                if (not self.bot.backupFlag):
                    self.bot.backupFlag = True
                    self.gis = GoogleImagesSearch(self.GOOGLE_BU, self.GOOGLE_CX) # now i have 200 queries/day
                else:
                    self.bot.backupFlag = False
                    self.gis = GoogleImagesSearch(self.GOOGLE_ID, self.GOOGLE_CX)
                try:
                    self.bot.gis.search(search_params=_search_params, path_to_dir="images/", custom_image_name='currentImage') # testing thingy
                except:
                    error_message = "out of queries for the day :/" # runs out quick?

            file = discord.File(fp, filename=filename)
            embed = discord.Embed(title=query, color=int(hex(int('f5a9b8', 16)), 0)) # color = f5a9b8, seems complicated?
            embed.set_footer(text=error_message)
            embed.set_image(url="attachment://currentImage.jpg")
            await ctx.reply(file=file,  embed=embed, mention_author=False)

            #print(str(type(self.bot.gis.results())) + " ; " + _search_params['q']) # more testing
            #await ctx.send(str(self.bot.gis.results())) # bullshit
        else:
            await ctx.reply("i can't search for nothing,,", mention_author=False) # making sure there's something to search

    @commands.command(name='cImage', hidden=True)
    @commands.is_owner()
    async def current_image(self, ctx):
        if (self.bot.currentNSFW and (not ctx.channel.is_nsfw())): # if the current image comes from an nsfw channel, you can't send it outside of those
            await ctx.reply("currentImage is nsfw, can't send here :/", mention_author=False)
        else:
            file = discord.File("images/currentImage.jpg", filename="currentImage.jpg")
            embed = discord.Embed(title="current image", color=int(hex(int('f5a9b8', 16)), 0)) # color = f5a9b8, seems complicated?
            embed.set_image(url="attachment://currentImage.jpg")
            await ctx.reply(file=file,  embed=embed, mention_author=False)
        


def setup(bot):
    bot.add_cog(BotCommands(bot))
