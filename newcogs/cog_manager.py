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
    async def show(self, ctx, cog=None):
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        extensions = []
        for extension in self.bot.extensions:
            extensions.append(extension.split('.')[1]+'.py')

        loadedembed = discord.Embed(title="Loaded Cogs", color=0xFFFFFF)
        unloadedembed = discord.Embed(title="Unloaded Cogs", color=0xFFFFFF)
        

        for f in os.listdir('./newcogs'):
            if f.endswith('.py'):
                if str(f) in extensions:
                    loadedembed.add_field(name=str(f), value='\u200b')
                else:
                    unloadedembed.add_field(name=str(f), value='\u200b')


        await ctx.send(embed=loadedembed)
        await ctx.send(embed=unloadedembed)


    @commands.command(pass_context=True, usage="load [cog]", hidden=True)
    async def load(self, ctx, cog=None):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        if cog == None:
            embed = discord.Embed(title="No cog", color=0xFD3333)
            await ctx.send(embed=embed)
            return
        
        self.bot.load_extension(f"newcogs.{cog}")
        await ctx.send(embed=discord.Embed(title="Loaded "+f"newcogs.{cog}", color=0x00FF42))


    @commands.command(pass_context=True, usage="unload [cog]", hidden=True)
    async def unload(self, ctx, cog=None):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        if cog == None:
            embed = discord.Embed(title="No cog", color=0xFD3333)
            await ctx.send(embed=embed)
            return

        self.bot.unload_extension(f"newcogs.{cog}")
        embed = discord.Embed(
            title="Unloaded "+f"newcogs.{cog}", color=0x00FF42)
        await ctx.send(embed=embed)


    @commands.command(pass_context=True, usage="reload [cog]", hidden=True)
    async def reload(self, ctx, cog=None):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        if cog == None:
            embed = discord.Embed(title="No cog", color=0xFD3333)
            await ctx.send(embed=embed)
            return

        self.bot.reload_extension(f"newcogs.{cog}")
        embed = discord.Embed(
            title="Reloaded "+f"newcogs.{cog}", color=0x00FF42)
        await ctx.send(embed=embed)


    @commands.command(pass_context=True, usage="reloadall", hidden=True)
    async def reloadall(self, ctx):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        extensions = []
        for extension in self.bot.extensions:
            extensions.append(extension.split('.')[1]+'.py')

       

        for f in os.listdir('./newcogs'):
            if f.endswith('.py'):
                cog = f"newcogs.{str(f)[:-3]}"
                if str(f) == 'uptime.py' or str(f) == 'cog_manager.py':
                    continue
                if str(f) in extensions:
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

        embed = discord.Embed(title="Reloaded "+" all cogs", color=0x00FF42)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, usage="sex", hidden=True)
    async def sex(self, ctx):
        #await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        for extension in self.bot.extensions:
            await ctx.send(extension)


# adding and removing commands
    @commands.command(pass_context=True, usage="showcommands", hidden=True)
    async def showcommands(self, ctx):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        enabledembed = discord.Embed(title="Enabled commands", color=0xFFFFFF)
        disablededembed = discord.Embed(title="Disabled commands", color=0xFFFFFF)
        enabled = {}
        disabled = {}
        for command in self.bot.commands:
            if command.cog_name == None:
                cogname = "None"
            else:
                cogname = command.cog_name

            if command.enabled:
                if cogname not in enabled.keys():
                    enabled[cogname] = ''
                enabled[cogname] += command.name+'\n'
            else:
                if cogname not in disabled.keys():
                    disabled[cogname] = ''
                disabled[cogname] += command.name+'\n'

        for key in enabled.keys():
            enabledembed.add_field(name=key, value=enabled[key])
        for key in disabled.keys():
            disablededembed.add_field(name=key, value=disabled[key])

        await ctx.send(embed=enabledembed)
        await ctx.send(embed=disablededembed)


    @commands.command(pass_context=True, usage="denable [command]", hidden=True)
    async def denable(self, ctx, command = None):
        #await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return
            
        if command == None:
            embed = discord.Embed(title="No command", color=0xFD3333)
            await ctx.send(embed=embed)
            return

        command_obj = self.bot.get_command(command)
        command_obj.update(enabled=True)
        await ctx.send(embed=discord.Embed(title=f"Added {command}", color=0x00FF42))


    @commands.command(pass_context=True, usage="ddisable [command]", hidden=True)
    async def ddisable(self, ctx, command = None):
        #await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return
            
        if command == None:
            embed = discord.Embed(title="No command", color=0xFD3333)
            await ctx.send(embed=embed)
            return
            
        command_obj = self.bot.get_command(command)
        command_obj.update(enabled=False)
        await ctx.send(embed=discord.Embed(title=f"Removed {command}", color=0x00FF42))
        

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
    bot.add_cog(cog_manager(bot))