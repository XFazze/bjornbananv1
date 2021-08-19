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


class cog_manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# loading and unloading extensions
    @commands.command(pass_context=True, usage="show", hidden=True)
    async def sshow(self, ctx, cog=None):
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        extensions = []
        for extension in self.bot.extensions:
            extensions.append(extension.split('.')[1]+"."+extension.split('.')[2]+'.py')

        loadedembed = discord.Embed(title="Loaded Cogs", color=0xFFFFFF)
        unloadedembed = discord.Embed(title="Unloaded Cogs", color=0xFFFFFF)

        for f0 in os.listdir('./cogv3'):
            loaded= ""
            unloaded = ""
            for f in os.listdir('./cogv3/'+str(f0)):
                if not f.endswith('.py'):
                    continue
                if str(f0)+"."+str(f) in extensions:
                    loaded += str(f)+'\n'
                else:
                    unloaded += str(f)+'\n'
            if len(loaded) > 0:
                loadedembed.add_field(name=str(f0), value=loaded)
            if len(unloaded) > 0:
                unloadedembed.add_field(name=str(f0), value=unloaded)

        await ctx.send(embed=loadedembed)
        await ctx.send(embed=unloadedembed)

    @commands.command(pass_context=True, usage="load [cog]", hidden=True)
    async def sload(self, ctx, cat=None, cog=None):
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        if cat == None or cog == None:
            embed = discord.Embed(title="No cat or cog", color=0xFD3333)
            await ctx.send(embed=embed)
            return

        self.bot.load_extension(f"cogv3.{cat}.{cog}")
        await ctx.send(embed=discord.Embed(title="Loaded "+f"cogv3.{cat}.{cog}", color=0x00FF42))

    @commands.command(pass_context=True, usage="unload [cog]", hidden=True)
    async def sunload(self, ctx, cat=None, cog=None):
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        if cat == None or cog == None:
            embed = discord.Embed(title="No cat or cog", color=0xFD3333)
            await ctx.send(embed=embed)
            return

        self.bot.unload_extension(f"cogv3.{cat}.{cog}")
        embed = discord.Embed(
            title="Unloaded "+f"cogv3.{cat}.{cog}", color=0x00FF42)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, usage="reload [cog]", hidden=True)
    async def sreload(self, ctx, cat=None,  cog=None):
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        if cat == None or cog == None:
            embed = discord.Embed(title="No cat or cog", color=0xFD3333)
            await ctx.send(embed=embed)
            return

        self.bot.reload_extension(f"cogv3.{cat}.{cog}")
        embed = discord.Embed(
            title="Reloaded "+f"cogv3.{cat}.{cog}", color=0x00FF42)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, usage="reloadall", hidden=True)
    async def sreloadall(self, ctx):
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        extensions = []
        for extension in self.bot.extensions:
            extensions.append(extension.split('.')[1]+"."+extension.split('.')[2]+'.py')

        for f0 in os.listdir('./cogv3'):
            for f in os.listdir('./cogv3/'+str(f0)):
                if not f.endswith('.py'):
                    continue

                cog = "cogv3."+str(f0)+f".{str(f)[:-3]}"
                if str(f) == 'uptime.py' or str(f) == 'cog_manager.py':
                    continue
                if str(f0)+"."+str(f) in extensions:
                    try:
                        self.bot.reload_extension(cog)
                    except:
                        embed = discord.Embed(
                            title="Broken cog: " + cog, color=0xFD3333)
                        await ctx.send(embed=embed)

                else:
                    try:
                        self.bot.load_extension(cog)
                    except:
                        embed = discord.Embed(
                            title="Broken cog: " + cog, color=0xFD3333)
                        await ctx.send(embed=embed)

        embed = discord.Embed(title="Reloaded all cogs", color=0x00FF42)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, usage="sex", hidden=True)
    async def ssex(self, ctx):
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        for extension in self.bot.extensions:
            await ctx.send(extension)
        await ctx.send("done")

    @commands.command(pass_context=True, usage="sex", hidden=True)
    async def removeoldcog(self, ctx):
        self.bot.unload_extension('newcogs.cog_manager')
        


def setup(bot):
    bot.add_cog(cog_manager(bot))
