from discord.ext import commands
from random import choice
heartsList = [":heart:",":orange_heart:",":yellow_heart:",":green_heart:",":blue_heart:",":purple_heart:",":brown_heart:",":white_heart:",":cupid:",":gift_heart:",":sparkling_heart:",":heartpulse:",":heartbeat:",":revolving_hearts:",":two_hearts:",":heart_exclamation:",":heart_decoration:"] #there's a finite amount of heart emojis, i don't need a separate file for them

class Info(commands.Cog, description="basic info"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='invite', help='sends invite link :>') # self explanatory
    async def invite(self, ctx):
        await ctx.reply("i heard you wanted to add me to your server! here's the link " + choice(heartsList) + "\nhttps://discord.com/oauth2/authorize?client_id=748302551933517835&permissions=260651150448&scope=bot", mention_author=False)

    @commands.command(name='github', help='github link for AbBot!')
    async def github(self, ctx):
        await ctx.reply("here you go! " + choice(heartsList) + "\nhttps://github.com/blampf/AbBot", mention_author=False)

def setup(bot):
    bot.add_cog(Info(bot))