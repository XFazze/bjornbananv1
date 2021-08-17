import discord
import json
import math
import time
from discord.ext import commands


class Join_leave_log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        filename = '/tmp/discordbot/logs/joinleave_logs/' + \
            str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " join " + str(member) + " " + str(member.guild.id) + "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " join " + str(member) + " " + str(member.guild.id) + "\n")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        filename = '/tmp/discordbot/logs/joinleave_logs/' + \
            str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " leave " + str(member) + " " + str(member.guild.id) + "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " leave " + str(member) + " " + str(member.guild.id) +  "\n")




def setup(bot):
    bot.add_cog(Join_leave_log(bot))