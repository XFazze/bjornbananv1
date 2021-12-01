import discord, datetime, time
from ..admin.managecommands import perms
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import random


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
# Ping
    
    @commands.command(pass_context=True, aliases=['latency'])
    async def ping(self, ctx):
        
        #await ctx.message.delete()
        embed = discord.Embed(colour=0xFFFFFF)
        embed.add_field(name="Latency", value='{0}ms'.format(round(self.bot.latency*1000, 1)))
        await ctx.reply(embed=embed)
    

def setup(bot):
    bot.add_cog(Ping(bot))