import discord, datetime, time
from ..admin.managecommands import perms
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import random


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


   
 

def setup(bot):
    bot.add_cog(Help(bot))