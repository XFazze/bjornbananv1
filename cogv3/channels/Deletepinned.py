import discord
import json
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
from discord.utils import get
import time
import os
import pymongo as pm


class Deletepinned(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Delete pinned
    @commands.command(pass_context=True, aliases=['edp'])
    @commands.has_permissions(manage_messages=True)
    async def enabledeletepinned(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]

        if ctx.channel.id in config["delete_pinned"]:
            embed = discord.Embed(
                title="Channel already added", color=0xFD3333)
            await ctx.send(embed=embed)

        else:
            config["delete_pinned"].append(ctx.channel.id)
            newvalue = {"$set": {"config": config}}
            collection.update_one(myquery, newvalue)
            embed = discord.Embed(
                title="Added channel to delete_pinned", color=0x00FF42)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['ddp'])
    @commands.has_permissions(manage_messages=True)
    async def disabledeletepinned(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]

        if ctx.channel.id in config["delete_pinned"]:
            config["delete_pinned"].remove(ctx.channel.id)
            newvalue = {"$set": {"config": config}}
            collection.update_one(myquery, newvalue)
            embed = discord.Embed(
                title="Removing channel from delete_pinned", color=0x00FF42)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Channel isn't in delete_pinned", color=0xFD3333)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.type.value == 6:
            collection = MongoClient('localhost', 27017).maindb.guilds
            myquery = {"id": ctx.guild.id}
            channels = collection.find_one(myquery)["config"]["delete_pinned"]
            for channel in channels:
                if channel == ctx.channel.id:
                    await ctx.delete()




def setup(bot):
    bot.add_cog(Deletepinned(bot))
