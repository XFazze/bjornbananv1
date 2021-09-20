import discord
from ..admin.managecommands import perms
import json
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
from discord.utils import get
import time
import os
import pymongo as pm


class Bettervc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidechannels.start()


# Bettervc
    @commands.command(pass_context=True, aliases=['eb'])
    @commands.has_permissions(manage_roles=True)
    @commands.check(perms)
    async def enablebettervc(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]
        
        
        if ctx.author.voice.channel.category_id in config["bettervc"]:
            embed = discord.Embed(
                title="Category already added", color=0xFD3333)
            await ctx.send(embed=embed)

        else:
            config["bettervc"].append(ctx.author.voice.channel.category_id)
            newvalue = {"$set": {"config": config}}
            collection.update_one(myquery, newvalue)
            embed = discord.Embed(
                title="Added category to bettervc", color=0x00FF42)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['db'])
    @commands.has_permissions(manage_roles=True)
    @commands.check(perms)
    async def disablebettervc(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]

        if ctx.author.voice.channel.category_id in config["bettervc"]:
            config["bettervc"].remove(ctx.author.voice.channel.category_id)
            newvalue = {"$set": {"config": config}}
            collection.update_one(myquery, newvalue)
            embed = discord.Embed(
                title="Removing category from bettervc", color=0x00FF42)
            await ctx.send(embed=embed)
        else:
            await ctx.send("category isn't in bettervc")

    @tasks.loop(seconds=5)
    async def hidechannels(self):
        collection = MongoClient('localhost', 27017).maindb.guilds
        guilds = collection.find({})
        for guild in guilds:
            guild_object = self.bot.get_guild(guild["id"])
            if len(guild["config"]["bettervc"]) != 0:
                for category in guild["config"]["bettervc"]:
                    category_object = get(self.bot.get_all_channels(), id=category)
                    
                    empty_channels = []
                    for channel in category_object.channels:
                        if len(channel.members) == 0 and channel.name[0] != '|':
                            empty_channels.append(channel)

                    showchannel = empty_channels.pop(0)
                    await showchannel.set_permissions(guild_object.default_role, overwrite=None)
                    await showchannel.set_permissions(guild_object.default_role, read_messages=True)
                    
                    for hiding_channel in empty_channels:
                        await hiding_channel.set_permissions(guild_object.default_role, read_messages=False)

    @hidechannels.before_loop
    async def before_hidechannels(self):
        print("Bettervc enabled")
        await self.bot.wait_until_ready()
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print("on_voice_state_update called")
        if after.channel is None:
            return
        print("on_voice_state_update didnt leave")
        collection = MongoClient('localhost', 27017).maindb.guilds
        guilds = collection.find_one({"id" : after.channel.guild.id})
        guild_object = self.bot.get_guild(guilds["id"])
        if after.channel.category_id in guilds["config"]["bettervc"] and before.channel == None:
            print("on_voice_state_update didnt category in bettervc and 1 member in channel")
            category_object = get(self.bot.get_all_channels(), id=after.channel.category_id)

            for empty_channel in category_object.channels:
                if len(empty_channel.members) == 0 and empty_channel.name[0] != '|':
                    print("on_voice_state_update found empty channel(row 101)")
                    await empty_channel.set_permissions(guild_object.default_role, overwrite=None)
                    await empty_channel.set_permissions(guild_object.default_role, read_messages=True)
                    return
            await category_object.create_voice_channel("waowie",guild_object.default_role, read_messages=True)


def setup(bot):
    bot.add_cog(Bettervc(bot))
