from discord.ext import commands
from random import choice
import sqlite3

from discord.ext.commands.core import has_permissions

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

    @commands.command(name='prefix', help='change the prefix! (ADMIN)', usage="<prefix>")
    @has_permissions(administrator=True)
    async def prefix(self, ctx, *args):
        if (args):
            con = sqlite3.connect('files/AbBotDatabase.db')
            cur = con.cursor()
            prefix = str(args[0][:5])
            cur.execute("update Guilds set Prefix=? where GuildID=?", (prefix, int(ctx.guild.id), ))
            con.commit()
            con.close()
            await ctx.reply("ok! my prefix has been changed to: `" + prefix + "`", mention_author=False)
        else:
            await ctx.reply("no prefix entered", mention_author=False)



def setup(bot):
    bot.add_cog(Info(bot))