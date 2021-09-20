import discord
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
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print("on_voice_state_update called")
        if after.channel is None:
            return
        print("on_voice_state_update didnt leave")
        collection = MongoClient('localhost', 27017).maindb.guilds
        guilds = collection.find_one({"id" : after.channel.guild.id})
        guild_object = self.bot.get_guild(802298523214938153)
        if before.channel == None:
            print("on_voice_state_update didnt category in bettervc and 1 member in channel")
            category_object = get(self.bot.get_all_channels(), id=after.channel.category_id)

            for empty_channel in category_object.channels:
                if len(empty_channel.members) == 0 and empty_channel.name[0] != '|':
                    print("on_voice_state_update found empty channel(row 101)")
                    await empty_channel.set_permissions(guild_object.default_role, overwrite=None)
                    return
            await category_object.create_voice_channel("waowie",guild_object.default_role, read_messages=None)


def setup(bot):
    bot.add_cog(Bettervc(bot))
