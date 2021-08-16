import discord
import json
from pymongo import MongoClient, collation
import pymongo as pm
from discord.ext import commands


class Mongodb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mdbguild(self, ctx):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return
        docs = []
        for guild in self.bot.guilds:
            text_channels = []
            for channel in guild.text_channels:
                if channel.category != None:
                    category = channel.category.name
                    category_id = channel.category_id
                else:
                    category = None
                    category_id = None

                text_channel = {
                    "id": channel.id,
                    "name": channel.name,
                    "category": category_id,
                    "category_id": category_id,

                }
                text_channels.append(text_channel)
            voice_channels = []
            for channel in guild.voice_channels:
                if channel.category != None:
                    category = channel.category.name
                    category_id = channel.category_id
                else:
                    category = None
                    category_id = None
                voice_channel = {
                    "id": channel.id,
                    "name": channel.name,
                    "category": category_id,
                    "category_id": category_id,
                }
                voice_channels.append(voice_channel)

            doc = {"name": guild.name,
                   "id": guild.id,
                   "text_channels": text_channels,
                   "voice_channels": voice_channels}
            docs.append(doc)

        db  = MongoClient('localhost', 27017).maindb
        collection = db.guilds
        collection.insert_many(docs)

    @commands.command(pass_context=True)
    async def mdbaddconfig(self, ctx):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        db = MongoClient('localhost', 27017).maindb
        collection = db.guilds
        for guild in self.bot.guilds:
            myquery = {"id" : guild.id}
            newvalues = {"$set" : {"config": {
                       "joinrole": [],
                       "prefix": ',',
                       "bettervc": [],
                       "delete_pinned": [],
                       "deletingchannel": [],
                   }}}
            doc = collection.update_one(myquery, newvalues)
            print("doc", doc)




def setup(bot):
    bot.add_cog(Mongodb(bot))
