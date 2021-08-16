from click import pass_context
import discord
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm


print("\nReloaded\n")



class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def a(self, ctx):
        print(dir(self.bot.commands))

    
    @commands.command(pass_context=True)
    async def b(self, ctx):
        for x in self.bot.commands:
            print(x)
        
    
    
    @commands.command(pass_context=True)
    async def c(self, ctx):
        print(self.bot.cogs.items)
        
    
    @commands.command(pass_context=True)
    async def d(self, ctx):
        print("")
        
        
    @commands.command(pass_context=True)
    async def e(self, ctx):
        print("")











def setup(bot):
    bot.add_cog(Test(bot))