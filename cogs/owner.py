import discord
from discord.ext import commands

helloFile = open("files/helloList.txt", "r") #opens a file to let you have as many or as few greetings as you'd like. allows for modularity in the bot without having to restart it every time you wanna add a greeting
helloList = helloFile.read().splitlines()
helloFile.close()

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addHi', hidden=True) # adds a greeting to files/helloList.txt
    @commands.is_owner()
    async def addHi(self, ctx, *args):            # if you're not me and you're running a copy of this, add your userID to the .env file
        if args != ():                      # i did "$dotenv set ADMIN_ID [userID]"
            newGreeting = '{}'.format(' '.join(args))
            if not (newGreeting in helloList):
                helloFile = open("files/helloList.txt", "a")
                helloFile.write(newGreeting + '\n')
                helloList.append(newGreeting)
                helloFile.seek(0)
                print(helloList) # debug code to make sure it all works properly
                helloFile.close()
                await ctx.send("**" + newGreeting + "** added to `helloList.txt`!")
            else:
                await ctx.send("**" + newGreeting + "** already in `helloList.txt`")

    @commands.command(name='removeHi', hidden=True) # in case i somehow get a bad greeting in there >:< (angy)
    @commands.is_owner()
    async def removeHi(self, ctx, *args):
        if args != ():
            badGreeting = '{}'.format(' '.join(args))
            if badGreeting in helloList:
                helloList.remove(badGreeting)
                helloFile = open("files/helloList.txt", "w")
                for greeting in helloList: # im sure there's a better way of fixing the list than this, but this is what i got right now. it sucks the larger the list gets
                    helloFile.write(greeting + '\n')
                helloFile.close()
                print(helloList)
                await ctx.send("done! you won't see **" + badGreeting + "** in there anymore!")
            else:
                await ctx.send("im not seeing **" + badGreeting + "** in the list,,")

    @commands.command(name='changeStatus', hidden=True) # gotta shake things up sometimes
    @commands.is_owner()
    async def changeStatus(self, ctx):
        await status_change()
        print("manually changed status at: " + time.strftime("%H:%M:%S", time.localtime()))
        await ctx.send("done!")

    @commands.command(name='loadCog', hidden=True) # taken from https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unloadCog', hidden=True) # taken from https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reloadCog', hidden=True) # taken from https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name="ownerCheck", hidden=True)
    @commands.is_owner()
    async def owner_check(self, ctx):
        await ctx.send(f'howdy {ctx.author.name}!')

def setup(bot):
    bot.add_cog(Owner(bot))
