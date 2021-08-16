import discord
import json
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
from discord.utils import get


class Better_vc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidechannels.start()

    @commands.command(pass_context=True, aliases=['eb'])
    @commands.has_permissions(manage_roles=True)
    async def enablebettervc(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]
        
        
        if ctx.author.voice.channel.category_id in config["bettervc"]:
            embed = discord.Embed(
                title="Category already decided, remove if changing", color=0xFD3333)
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

    @tasks.loop(seconds=10)
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
                        if len(channel.members) == 0:
                            empty_channels.append(channel)
                    empty_channels.pop(0)
                    for hiding_channel in empty_channels:
                        await hiding_channel.set_permissions(guild_object.default_role, read_messages=False)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        collection = MongoClient('localhost', 27017).maindb.guilds
        guilds = collection.find_one({"id" : after.channel.guild.id})
        guild_object = self.bot.get_guild(guilds["id"])
        if after.channel.category_id in guilds["config"]["bettervc"] and len(after.channel.members) == 1:
            category_object = get(self.bot.get_all_channels(), id=after.channel.category_id)
            for empty_channel in category_object.channels:
                if len(empty_channel.members) == 0:
                    await empty_channel.set_permissions(guild_object.default_role, read_messages=None)
                    break
    
       

    @hidechannels.before_loop
    async def before_hidechannels(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Better_vc(bot))
