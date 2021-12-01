from re import L
import discord
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import git
import pymongo as pm


class MongoDB(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mdbguildloop.start()



# Mongo DB

    @commands.command(pass_context=True)
    async def mdbguildupdate(self, hidden=True):
        db = MongoClient('localhost', 27017).maindb
        collection = db.guilds

        for guild in self.bot.guilds:
            myquery = {"id": guild.id}
            doc = collection.find_one(myquery)
            create = False
            if doc == None:
                create = True
                doc = {
                    "id": guild.id,
                    "name": guild.name
                }

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

            doc["text_channels"] = text_channels
            doc["voice_channels"] = voice_channels
            if "config" not in doc.keys():
                doc["config"] = {}
            if "joinrole" not in doc["config"].keys():
                doc["config"]["joinrole"] = []
            if "prefix" not in doc["config"].keys():
                doc["config"]["prefix"] = ','
            if "bettervc" not in doc["config"].keys():
                doc["config"]["bettervc"] = []
            if "delete_pinned" not in doc["config"].keys():
                doc["config"]["delete_pinned"] = []
            if "deletingchannel" not in doc["config"].keys():
                doc["config"]["deletingchannel"] = []
            if "joinleavemessage" not in doc["config"].keys():
                doc["config"]["joinleavemessage"] = []

            if "settings" not in doc.keys():
                doc["settings"] = {}

            if create:
                collection.insert_one(doc)
            else:
                myquery = {"id": guild.id}
                collection.replace_one(myquery, doc)

    @commands.command(pass_context=True)
    async def dmdbguild(self, ctx, hidden=True):
        if not str(ctx.author) == "mega#5630" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.reply("Youre noone")
            return
        await self.mdbguildupdate()
        await ctx.reply(embed=discord.Embed(title="Successfully updated mongodbguild", color=0x00FF42))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.mdbguildupdate()

    @tasks.loop(seconds=120)
    async def mdbguildloop(self):
        await self.mdbguildupdate()

    @mdbguildloop.before_loop
    async def before_cleanse(self):
        print('mongodbguildupdate enabled')
        await self.bot.wait_until_ready()



def setup(bot):
    bot.add_cog(MongoDB(bot))
