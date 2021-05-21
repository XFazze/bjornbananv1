import discord
import time
import math
import os
import json
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ts(self, ctx):
        with open('/home/pi/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "tcstats" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return

        directory = os.fsencode('/home/pi/discordbot/logs/tc_logs/')
        bigfileline = []
        for file in os.listdir(directory):
            filename = '/home/pi/discordbot/logs/tc_logs/'+os.fsdecode(file)
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


def setup(bot):
    bot.add_cog(Base(bot))
