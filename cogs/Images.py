from discord.ext import commands
from google_images_search import GoogleImagesSearch
from pathlib import Path
import random
from os import remove
import requests
import discord

albumList = list()
albumList2 = list()

 # for <iSearch
_search_params = {
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

class Images(commands.Cog, description="all of the commands that deal with images"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='notCat', help="cat pix", hidden=True) # gonna be <sebby if i get the imgur link for it
    #@commands.is_nsfw()                        # for now it's a doujin
    async def not_cat(self, ctx):               # doesn't need to exist since i have <imgur, but oh well, im keeping it
        if ctx.channel.is_nsfw(): 
            url = "https://api.imgur.com/3/album/J3bm5gs/images"
            albumList.clear()
            response = requests.request("GET", url=url, headers={'Authorization': 'Client-ID {}'.format(self.bot.IMGUR_ID)}, data={}, files={})
            for i in response.json()['data']:
                albumList.append(i['link'])
            await ctx.reply(str(random.choice(albumList)), mention_author=False)
        else:
            await ctx.reply("currently an nsfw command ;>", mention_author=False)


    @commands.command(name='iSearch', help='google image search!', usage='<search terms>')
    async def image_search(self, ctx, *args):
        if args != "":
            query = "{}".format(" ".join(args)) # this and the above line are copied from the google search command
            query = query.replace("'", "")
            query = query.replace("’", "")
            _search_params['q'] = query         # modifying the dictionary
            self.bot.imageDesc = query
            if ctx.channel.is_nsfw(): 
                _search_params['safe'] = 'off'
                self.bot.currentNSFW = True # not robust because it doesn't have to be
            else:
                _search_params['safe'] = 'medium'
                self.bot.currentNSFW = False
            error_message = ""
            filename = "currentImage.jpg"
            fp = "images/currentImage.jpg"
            file_path = Path("images/currentImage.jpg") # deleting current currentImage.jpg
            if file_path.is_file():
                try:
                    remove(file_path)
                except OSError as e:
                    filename = "currentImage(1).jpg"
                    fp = "images/currentImage(1).jpg"
                    print("Error: %s : %s" % (file_path, e.strerror))
            try:
                self.bot.gis.search(search_params=_search_params, path_to_dir="images/", custom_image_name='currentImage') # testing thingy

            except: # something complicated to get around the 100 queries/day
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
            embed = discord.Embed(title=query, color=0xf5a9b8) # color = f5a9b8, seems complicated?
            embed.set_footer(text=error_message)
            embed.set_image(url="attachment://currentImage.jpg")
            await ctx.reply(file=file,  embed=embed, mention_author=False)
        else:
            await ctx.reply("i can't search for nothing,,", mention_author=False) # making sure there's something to search

    @commands.command(name='cImage', hidden=True, usage='<cimage')
    @commands.is_owner()
    async def current_image(self, ctx):
        if (self.bot.currentNSFW and (not ctx.channel.is_nsfw())): # if the current image comes from an nsfw channel, you can't send it outside of those
            await ctx.reply("currentImage is nsfw, can't send here :/", mention_author=False)
        else:
            file = discord.File("images/currentImage.jpg", filename="currentImage.jpg")
            embed = discord.Embed(title="current image", description=self.bot.imageDesc, color=0xf5a9b8) # color = #f5a9b8, seems complicated?
            embed.set_image(url="attachment://currentImage.jpg")
            await ctx.reply(file=file, embed=embed, mention_author=False)

    @commands.command(name='Imgur', help="sends an image from an imgur album! (defaults to cats)", usage='[imgur album url/ID]')
    async def imgur(self, ctx, *args):
        string = random.choice(["Jfni3", "8DqtFI3", "LMQtP9m"])
        if args != ():
            string = args[0]
            if ("https://imgur.com/gallery/" in string):
                string = string.split('/')[4] # separating the url into blocks, picking the albumID one
            elif (".jpeg" or ".png" or ".gif") in string:
                await ctx.reply(string, mention_author=False)
                return
        url = "https://api.imgur.com/3/album/{}/images".format(string)
        albumList2.clear()
        response = requests.request("GET", url=url, headers={'Authorization': 'Client-ID {}'.format(self.bot.IMGUR_ID)}, data={}, files={})
        for i in response.json()['data']:
            albumList2.append(i['link'])
        await ctx.reply(str(random.choice(albumList2)), mention_author=False)
        # at a certain point, i need more cogs


def setup(bot):
    bot.add_cog(Images(bot))