import discord
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import git
import pymongo as pm
import datetime

start_time = time.time()


class uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Uptime
    
    @commands.command(pass_context=True, name="uptime", aliases=[], description="", usage="uptime")
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xFFFFFF)
        embed.add_field(name="Uptime", value=text)
        try:
            await ctx.reply(embed=embed)
        except discord.HTTPException:
            await ctx.reply("Current uptime: " + text)


def setup(bot):
    bot.add_cog(uptime(bot))