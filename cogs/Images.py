from discord.ext import commands
from google_images_search import GoogleImagesSearch
import random
from os import remove, listdir
import requests
import discord
import requests, random
from json.decoder import JSONDecodeError as jsdecode

albumList = list()
albumList2 = list()

 # for <iSearch
_search_params = {
    'q': '...',
    'num': 1,
    'safe': 'off',
    'fileType': 'png|jpg'
    #'imgType': 'clipart|face|lineart|news|photo',
    #'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge',
    #'imgDominantColor': 'black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow',
    #'imgColorType': 'color|gray|mono|trans',
    #'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
}

def booruSearch(searchCode: int, taglist: list) -> str:
    '''returns a url based on search terms entered'''
    tagstr = ""
    tagLim = len(taglist)
    if (searchCode == 0 and len(taglist) > 1): # danbooru only lets you search for 2 tags at a time
        tagLim = 2
    for iter in range(tagLim): # appending all the tags to a single string for ease of use
        tagstr += taglist[iter] + "+"
    
    # html page request, grabs the page, steals the json
    # each site has their own different style requiring different vars
    if (searchCode == 1):
        limit = 3000
        url = f'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit={limit}&tags={tagstr}'
    elif (searchCode == 2):
        limit = 1000
        url = f'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit={limit}&tags={tagstr}'
    else:
        page = 1
        limit = 200
        url = f'https://danbooru.donmai.us/posts.json?page={page}&limit={limit}&[tags]={tagstr}'
    try:
        search = requests.get(url).json()
        if (searchCode == 1):
            search = search['post']
    except:
        return "Found none :/"

    # if there's no search results, let the user know and end
    if (len(search) == 0):
        return "Found none :/"
    
    # print(f'results: {len(search)}')

    image = ""

    # loop until you get a valid image url
    # because for some reason some posts just don't have image links?
    while (image == ""):
        # pick a random one from the selection
        randImg = random.choice(search)

        # take the random selection's image url
        try:
            # this only works on danbooru
            image = randImg["large_file_url"]
        except KeyError:
            # this should work on all of them
            image = randImg["file_url"]
    return image


def tagFormat(input: list) -> list:
    '''formats sys.argv[2:] to something useable by booruSearch'''
    # converts to a list of strings with no excess whitespace or commas
    # e.g. "fish feet, bone" becomes ["fish feet", "bone"]
    lst = " ".join(input).strip().split(",")
    retList = []
    for item in lst:
        # turns spaces into underscores
        # e.g. ["fish feet", "bone"] becomes ["fish_feet", "bone"]
        retList.append("_".join(item.strip().split(" ")))
    return retList

class Images(commands.Cog, description="all of the commands that deal with images"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='iSearch', help='google image search!', usage='<search terms>')
    async def image_search(self, ctx, *args):
        if args != "":
            filename = ""
            fp = ""
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
            file_path = listdir("images/") # deleting current currentImage
            for item in file_path:
                #if item.startswith("currentImage"):
                remove("images/" + item)
 
            '''if file_path.is_file(): # kinda hate all of this
                try:
                    remove(file_path)
                except OSError as e:
                    filename = "currentImage(1).jpg"
                    fp = "images/currentImage(1).jpg"
                    print("Error: %s : %s" % (file_path, e.strerror))'''
            try:
                self.bot.gis.search(search_params=_search_params, path_to_dir="images/")#, custom_image_name='currentImage') # testing thingy

            except: # something complicated to get around the 100 queries/day
                if (not self.bot.backupFlag):
                    self.bot.backupFlag = True
                    self.gis = GoogleImagesSearch(self.bot.GOOGLE_ID, self.bot.GOOGLE_CX) # now i have 200 queries/day
                else:
                    self.bot.backupFlag = False
                    self.gis = GoogleImagesSearch(self.bot.GOOGLE_ID, self.bot.GOOGLE_CX)
                try:
                    self.bot.gis.search(search_params=_search_params, path_to_dir="images/")#, custom_image_name='currentImage') # testing thingy
                except:
                    error_message = "out of queries for the day :/" # runs out quick?

            file_path = listdir("images/")
            for item in file_path:
                #if item.startswith("currentImage"):
                fp = "images/" + item
                filename = item

            file = discord.File(fp, filename=filename)
            embed = discord.Embed(title=query, color=0xf5a9b8) # color = f5a9b8, seems complicated?
            embed.set_footer(text=error_message)
            embed.set_image(url=f"attachment://{filename}")
            await ctx.reply(file=file, embed=embed, mention_author=False)
        else:
            await ctx.reply("i can't search for nothing,,", mention_author=False) # making sure there's something to search

    @commands.command(name='cImage', hidden=True, usage='<cimage')
    @commands.is_owner()
    async def current_image(self, ctx):
        if (self.bot.currentNSFW and (not ctx.channel.is_nsfw())): # if the current image comes from an nsfw channel, you can't send it outside of those
            await ctx.reply("currentImage is nsfw, can't send here :/", mention_author=False)
        else:
            filename = ""
            fp = ""
            file_path = listdir("images/")
            for item in file_path:
                #if item.startswith("currentImage"):
                fp = "images/" + item
                filename = item
            file = discord.File(fp, filename=filename)
            embed = discord.Embed(title="current image", description=self.bot.imageDesc, color=0xf5a9b8) # color = #f5a9b8, seems complicated?
            embed.set_image(url="attachment://" + filename)
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

    @commands.command(name='danbooru', help='danbooru search!', usage='<danbooru tags, comma seperated>')
    async def danbooru_search(self, ctx, *args):
        if not ctx.channel.is_nsfw():
            return await ctx.reply("this command is nsfw, try this somewhere else")
        elif args == ():
            return await ctx.reply("i can't search for nothing,,", mention_author=False)
        taglist = tagFormat(args)
        reply = booruSearch(0, taglist)
        await ctx.reply(reply, mention_author=False)
    
    @commands.command(name='gelbooru', help='gelbooru search!', usage='<gelbooru tags, comma seperated>')
    async def gelbooru_search(self, ctx, *args):
        if not ctx.channel.is_nsfw():
            return await ctx.reply("this command is nsfw, try this somewhere else")
        elif args == ():
            return await ctx.reply("i can't search for nothing,,", mention_author=False)
        taglist = tagFormat(args)
        reply = booruSearch(1, taglist)
        await ctx.reply(reply, mention_author=False)

    @commands.command(name='r34', help='rule34 search!', usage='<r34 tags, comma seperated>')
    async def r34_search(self, ctx, *args):
        if not ctx.channel.is_nsfw():
            return await ctx.reply("this command is nsfw, try this somewhere else")
        elif args == ():
            return await ctx.reply("i can't search for nothing,,", mention_author=False)
        taglist = tagFormat(args)
        reply = booruSearch(2, taglist)
        await ctx.reply(reply, mention_author=False)


def setup(bot):
    bot.add_cog(Images(bot))