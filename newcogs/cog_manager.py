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




class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Cog manager
    @commands.command(pass_context=True)
    async def showcogs(self, ctx, category=None, cog=None):
        #await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        extensions = []
        for extension in self.bot.extensions:
            extensions.append(extension.split(
                '.')[1] + '.' + extension.split('.')[2]+'.py')

        loadedembed = discord.Embed(title="Loaded Cogs", color=0xFFFFFF)
        unloadedembed = discord.Embed(title="Unloaded Cogs", color=0xFFFFFF)
        if len(os.listdir('./newcogs')) > 1:
            for f in os.listdir('./newcogs'):
                if f.endswith('.py'):
                    continue

                title = str(f)
                loadedcommands = ''
                unloadedcommands = ''
                for f in os.listdir('./cogs/'+title):
                    if f.endswith('.py'):
                        if title+'.'+str(f) in extensions:
                            loadedcommands += str(f)+'\n'
                        else:
                            unloadedcommands += str(f)+'\n'

                if len(loadedcommands) != 0:
                    loadedembed.add_field(name=title, value=loadedcommands)
                if len(unloadedcommands) != 0:
                    unloadedembed.add_field(name=title, value=unloadedcommands)

        await ctx.send(embed=loadedembed)
        await ctx.send(embed=unloadedembed)


    @commands.command(pass_context=True)
    async def loadcog(self, ctx, category=None, cog=None):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        if category == None or cog == None:
            embed = discord.Embed(title="No category or cog", color=0xFD3333)
            await ctx.send(embed=embed)
            return
        print(f"cogs.{category}.{cog}")
        self.bot.load_extension(f"cogs.{category}.{cog}")
        embed = discord.Embed(
            title="Loaded "+f"cogs.{category}.{cog}", color=0x00FF42)
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def unloadcog(self, ctx, category=None, cog=None):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        if category == None or cog == None:
            embed = discord.Embed(title="No category or cog", color=0xFD3333)
            await ctx.send(embed=embed)
            return

        self.bot.unload_extension(f"cogs.{category}.{cog}")
        embed = discord.Embed(
            title="Unloaded "+f"cogs.{category}.{cog}", color=0x00FF42)
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def reloadcog(self, ctx, category=None, cog=None):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        if category == None or cog == None:
            embed = discord.Embed(title="No category or cog", color=0xFD3333)
            await ctx.send(embed=embed)
            return

        self.bot.unload_extension(f"cogs.{category}.{cog}")
        self.bot.load_extension(f"cogs.{category}.{cog}")
        embed = discord.Embed(
            title="Reloaded "+f"cogs.{category}.{cog}", color=0x00FF42)
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def reloadall(self, ctx):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        extensions = []
        for extension in self.bot.extensions:
            extensions.append(extension.split(
                '.')[1] + '.' + extension.split('.')[2]+'.py')

        if len(os.listdir('./cogs')) > 1:
            for f in os.listdir('./cogs'):
                if f.endswith('.py'):
                    continue

                title = str(f)
                for f in os.listdir('./cogs/'+title):
                    if f.endswith('.py'):
                        cog = f"cogs.{title}.{str(f)[:-3]}"
                        if str(f) == 'uptime.py' or str(f) == 'cog_manager.py':
                            continue
                        if title+'.'+str(f) in extensions:
                            try:
                                self.bot.unload_extension(cog)
                                self.bot.load_extension(cog)
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

        embed = discord.Embed(title="Reloaded "+" all cogs", color=0x00FF42)
        await ctx.send(embed=embed)

# Uptime
    
    @commands.command(pass_context=True, name="uptime", aliases=[], description="", usage="uptime")
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xFFFFFF)
        embed.add_field(name="Uptime", value=text)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)


def setup(bot):
    bot.add_cog(Dev(bot))