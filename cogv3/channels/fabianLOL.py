import discord
from itsdangerous import exc
from ..admin.managecommands import perms
import json
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
from discord.utils import get
import time
import os
import pymongo as pm


class fabianLOL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Role log
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.channel.id == 936101882387103765 and ctx.author != self.bot.user:
            try:
                num = int(ctx.content)
            except:
                return
            await ctx.reply(f'{num}/3600, WINS: {(3600-num)/5}  LOSSES: {(3600-num)/10}')
            await ctx.delete()





def setup(bot):
    bot.add_cog(fabianLOL(bot))
