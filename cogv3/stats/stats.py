import discord
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import math


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# TC stats
    @commands.command(pass_context=True, aliases=['tc', 'tcstats'], enabled= False)
    async def textstats(self, ctx):
        with open('/tmp/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "tcstats" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return

        directory = os.fsencode('/tmp/discordbot/logs/tc_logs/')
        bigfileline = []
        for file in os.listdir(directory):
            filename = '/tmp/discordbot/logs/tc_logs/'+os.fsdecode(file)
            with open(filename, 'r') as file:
                filelines = file.readlines()
                for line in filelines:
                    bigfileline.append(line)

        messages = {}

        for line in bigfileline:
            linelist = line.split(" ")
            if linelist[1] == "send":
                name = str(linelist[5])[:-1]
                if name in messages.keys():
                    messages[name] = messages[name]+1
                else:
                    messages[name] = 1

        messages = dict(sorted(messages.items(), key=lambda item: item[1]))
        mess = ""
        for item in messages:
            mess = mess + str(messages[item]) + "   :   " + str(item) + "\n"
        await ctx.send(mess)
    

# VC stats 
    @commands.command(pass_context=True, aliases=['vc', 'vcstats'], enabled= False)
    async def vs(self, ctx):
        with open('/tmp/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "vcstats" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return

        directory = os.fsencode('/tmp/discordbot/logs/vc_logs/')
        bigfileline = []
        for file in os.listdir(directory):
            filename = '/tmp/discordbot/logs/vc_logs/'+os.fsdecode(file)
            with open(filename, 'r') as file:
                filelines = file.readlines()
                for line in filelines:
                    bigfileline.append(line)
        minutes = {}
        for line in bigfileline:
            linelist = line.split(" ")
            if linelist[1] == "connect":
                line_num = bigfileline.index(line)
                for iline in bigfileline[line_num:]:
                    ilinelist = iline.split(" ")
                    if ilinelist[1] == "disconnect" and str(linelist[3])[:-1] == str(ilinelist[3])[:-1]:
                        trime = int(math.floor(
                            (float(ilinelist[0])/60 - float(linelist[0])/60)))
                        name = str(linelist[3])[:-1]
                        if name in minutes.keys():
                            minutes[name] = minutes[name]+trime
                        else:
                            minutes[name] = trime
                        break

        minutes = dict(sorted(minutes.items(), key=lambda item: item[1]))
        mess = ""
        for item in minutes:
            mess = mess + str(minutes[item]) + "   :   "+str(item)+"\n"
        await ctx.send(mess)
    

def setup(bot):
    bot.add_cog(Stats(bot))