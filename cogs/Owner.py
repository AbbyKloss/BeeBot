import discord
from discord.ext import commands
from discord.ext import tasks
import time
import random

helloFile = open("files/helloList.txt", "r") #opens a file to let you have as many or as few greetings as you'd like. allows for modularity in the bot without having to restart it every time you wanna add a greeting
helloList = helloFile.read().splitlines()
helloFile.close()

# randomize statuses so it doesn't feel so static
gameStatuses = ["with your heart💙", "critically acclaimed mmorpg final fantasy fourt teen", "fin fant " + str(random.randrange(1, 15)), "monstie huntie", "lelda of zelda breath of the weath"]
musicStatuses = ["number 1 victory royale yeah fortnite we boutta get down (get down) 10 kills on the board right now just wiped out tomato town", "spoofy", "music on the you tubes", "tidal (i love jay z)", "More Dunkey More Problems", "bent knee live on twiiiitch, bent knee livestreamiiing"]
videoStatuses = ["idk some ding dong video on the you tube", "demons layer ;>", "vine land saga", "zombie vine land saga"]


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.the_loop.start()

    async def status_change(self): # randomizes statuses every hour (and also on startup :> )
        choice = random.randint(1, 3) # roll 1d3 nerd
        if choice == 1:   # playing
            await self.bot.change_presence(activity=discord.Game(random.choice(gameStatuses)))
        elif choice == 2: # listening
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(musicStatuses)))
        elif choice == 3: # watching
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(videoStatuses)))

    @tasks.loop(hours=1)
    async def the_loop(self):
        print("automatically changed status at: " + time.strftime("%H:%M:%S", time.localtime())) # prints to the console so you know the status actually changed with a timestamp so you know when
        await self.status_change()

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
        await self.status_change(self)
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

    @commands.command(name="customStatus", hidden=True)
    @commands.is_owner()
    async def custom_status(self, ctx, statusType=0, streamlink='NONE', *args):
        if (int(statusType) <= 4) and (int(statusType) >= 1):
            if args != ():
                self.the_loop.cancel()
                print("stopped loop at: " + time.strftime("%H:%M:%S", time.localtime()))
                status = '{}'.format(' '.join(args))
                if statusType == 1:
                    await self.bot.change_presence(activity=discord.Game(name=status))

                if statusType == 2:
                    await self.bot.change_presence(activity=discord.Streaming(name=status, url=streamlink, game=status, details=status))

                if statusType == 3:
                    await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))

                if statusType == 4:
                    await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
                await ctx.send('done!')
            else:
                await ctx.send('you gotta give me something to work with')
        else:
            await ctx.send('no type/wrong type')

    @commands.command(name='resumeTheLoop', hidden=True)
    @commands.is_owner()
    async def resume_the_loop(self, ctx):
        self.the_loop.start()
        await ctx.send('The Loop Has Resumed.')

    @commands.command(name="testPrint", hidden=True)
    @commands.is_owner()
    async def test_print(self, ctx, *args):
        if args != ():
            printable = '{}'.format(' '.join(args))
            print('\n' + printable + '\n')
            await ctx.send('done!')

def setup(bot):
    bot.add_cog(Owner(bot))
