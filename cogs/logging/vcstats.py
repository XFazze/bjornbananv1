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
    async def vcstats(self, ctx):
        with open('/home/pi/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "vcstats" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return

        directory = os.fsencode('/home/pi/discordbot/vc_logs/')
        bigfileline = []
        for file in os.listdir(directory):
            filename = '/home/pi/discordbot/vc_logs/'+os.fsdecode(file)
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
    bot.add_cog(Base(bot))
