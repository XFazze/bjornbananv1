import discord
from pymongo import MongoClient
from discord.ext import commands


class cogName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, aliases=[])
    async def commandName(self, ctx):
        pass

def setup(bot):
    bot.add_cog(cogName(bot))