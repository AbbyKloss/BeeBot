import discord
from discord.ext import commands

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if ("cope" in message.content.lower()):
            emoji = '<:COPE:848006983726530601>'
            await message.add_reaction(emoji)

        if ("hope" in message.content.lower()):
            emoji = '<:HOPE:848007900517629973>'
            await message.add_reaction(emoji)

        if ("turtle" in message.content.lower()) or ("turble" in message.content.lower()) or ("tortle" in message.content.lower()) or ("🐢" in message.content.lower() or ("turdle" in message.content.lower())):
            emoji = '<:turble:848677634577006643>'
            await message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(Listeners(bot))
