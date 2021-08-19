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


class Ratelimited(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Ratelimited

    @commands.Cog.listener()
    async def is_ws_ratelimited(self):
        print("Being websocket ratelimited")



def setup(bot):
    bot.add_cog(Ratelimited(bot))
