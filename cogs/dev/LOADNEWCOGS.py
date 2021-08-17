import discord
from discord.ext import commands
import os


class Cog_manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def loadnewcogs(self, ctx):
        self.bot.load_extension("newcogs.cog_manager")
        await ctx.send("loaded newcogs.cog_manager")


def setup(bot):
    bot.add_cog(Cog_manager(bot))
