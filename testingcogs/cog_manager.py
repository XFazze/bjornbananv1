import discord
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import git
import pymongo as pm







class Cog_manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def loadcog(self, ctx, cog):
        print("hej")

    
    
    
    
    




def setup(bot):
    bot.add_cog(Cog_manager(bot))