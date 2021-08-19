import discord
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import math
import random

class Diceroll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
          

# Diceroll
    @commands.command(pass_context=True, aliases=[])
    async def diceroll(self, ctx, dice:int = 6):
      await ctx.send(embed=discord.Embed(title="You got an " + str(random.randint(0,dice)), color=0x00FF42))
    
    
    


def setup(bot):
    bot.add_cog(Diceroll(bot))