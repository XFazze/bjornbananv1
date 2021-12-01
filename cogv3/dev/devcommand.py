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


class devcommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# adding and removing commands
    @commands.command(pass_context=True, usage="showcommands", hidden=True)
    async def showcommands(self, ctx):
        if not str(ctx.author) == "mega#5630" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.reply("Youre noone")
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

        await ctx.reply(embed=enabledembed)
        await ctx.reply(embed=disablededembed)


    @commands.command(pass_context=True, usage="denable [command]", hidden=True)
    async def denable(self, ctx, command = None):
        #await ctx.message.delete()
        if not str(ctx.author) == "mega#5630" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.reply("Youre noone")
            return
            
        if command == None:
            embed = discord.Embed(title="No command", color=0xFD3333)
            await ctx.reply(embed=embed)
            return

        command_obj = self.bot.get_command(command)
        command_obj.update(enabled=True)
        await ctx.reply(embed=discord.Embed(title=f"Added {command}", color=0x00FF42))


    @commands.command(pass_context=True, usage="ddisable [command]", hidden=True)
    async def ddisable(self, ctx, command = None):
        #await ctx.message.delete()
        if not str(ctx.author) == "mega#5630" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.reply("Youre noone")
            return
            
        if command == None:
            embed = discord.Embed(title="No command", color=0xFD3333)
            await ctx.reply(embed=embed)
            return
            
        command_obj = self.bot.get_command(command)
        command_obj.update(enabled=False)
        await ctx.reply(embed=discord.Embed(title=f"Removed {command}", color=0x00FF42))
        

def setup(bot):
    bot.add_cog(devcommand(bot))