import discord
from ..admin.managecommands import perms
import json
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
from discord.utils import get
import time
import os
import pymongo as pm


class Deletingchannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cleanse.start()

# Deletingchannel

    @commands.command(pass_context=True, aliases=['ed'])
    @commands.has_permissions(manage_messages=True)
    @commands.check(perms)
    async def enabledelete(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]

        if ctx.channel.id in config["deletingchannel"]:
            embed = discord.Embed(
                title="Channel already added", color=0xFD3333)
            await ctx.reply(embed=embed)

        else:
            config["deletingchannel"].append(ctx.channel.id)
            newvalue = {"$set": {"config": config}}
            collection.update_one(myquery, newvalue)
            embed = discord.Embed(
                title="Added channel to deletingchannel", color=0x00FF42)
            await ctx.reply(embed=embed)

    @commands.command(pass_context=True, aliases=['dd'])
    @commands.has_permissions(manage_messages=True)
    @commands.check(perms)
    async def disabledelete(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]

        if ctx.channel.id in config["deletingchannel"]:
            config["deletingchannel"].remove(ctx.channel.id)
            newvalue = {"$set": {"config": config}}
            collection.update_one(myquery, newvalue)
            embed = discord.Embed(
                title="Removing channel from deletingchannel", color=0x00FF42)
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title="Channel isn't in deletingchannel", color=0xFD3333)
            await ctx.reply(embed=embed)

    @tasks.loop(seconds=5) 
    async def cleanse(self):
        collection = MongoClient('localhost', 27017).maindb.guilds
        guilds = collection.find({})
        for guild in guilds:
            guild_object = self.bot.get_guild(guild["id"])
            if len(guild["config"]["deletingchannel"]) != 0:
                for channelid in guild["config"]["deletingchannel"]:
                    channel_obj = get(self.bot.get_all_channels(), id=channelid)
                    messages = await channel_obj.history(limit=100).flatten()
                    await channel_obj.delete_messages(messages)
       

    @cleanse.before_loop
    async def before_cleanse(self):
        print('deletingchannel enabled')
        await self.bot.wait_until_ready()




def setup(bot):
    bot.add_cog(Deletingchannel(bot))
