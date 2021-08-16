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


    @commands.command(pass_context=True)
    async def cogs(self, ctx):
        #loaded_cogs = discord.Embed(title="Loaded cogs", color=0x00FF42)
        #unloaded_cogs = discord.Embed(title="Unloaded cogs", color=0xFD3333)

        loaded_cogs = []
        
        for cog in self.bot.cogs:
            loaded_cogs.append(cog)
        
        embed1 = discord.Embed(title=f"Loaded cogs: ```{loaded_cogs}```", color=0x00FF42)
        await ctx.send(embed=embed1)
        
        
        #self.bot.remove_cog("Test")
        
        
        cogs = []
        unloaded_cogs = []
        
        for f in os.listdir("testingcogs"):
            if f.endswith(".py"):
                f = f[:-3]
                cogs.append(f)
        
        for x in cogs:
            x = str(x).capitalize()
            if x not in loaded_cogs:
                unloaded_cogs.append(x)
        
        embed2 = discord.Embed(title=f"Unloaded cogs: ```{unloaded_cogs}```", color=0xFD3333)
        await ctx.send(embed=embed2)
        
                
        
        
            

    @commands.command(pass_context=True)
    async def load(self, ctx, cog):
        if cog == None:
            embed = discord.Embed(title="Specify a cog", color=0xFD3333)
            await ctx.send(embed=embed)
    
        try:
            self.bot.add_cog(cog)
            embed = discord.Embed(title=f"Loaded cog ```{cog}```", color=0x00FF42)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title=f"Cog ```{cog}``` doesn't exist or is already loaded", color=0xFD3333)
            await ctx.send(embed=embed)
    
    
    @commands.command(pass_context=True)
    async def unload(self, ctx, cog = None):
        if cog == None:
            embed = discord.Embed(title="Specify a cog", color=0xFD3333)
            await ctx.send(embed=embed)
            
        try:
            self.bot.remove_cog(str(cog))
            embed = discord.Embed(title=f"Unloaded cog ```{cog}```", color=0x00FF42)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title=f"Cog ```{cog}``` is not loaded", color=0xFD3333)
            await ctx.send(embed=embed)
        
        
    '''@commands.command(pass_context=True)
    async def reload(self, ctx, cog):
        print("bitch")
    
    
    @commands.command(pass_context=True)
    async def reloadall(self, ctx):
        print("bitch")'''

    
    
    
    
    




def setup(bot):
    bot.add_cog(Cog_manager(bot))