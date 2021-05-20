import discord
import json
import math
import time
import os
from datetime import datetime
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_message(self, ctx):
        jsonf = {
                    "content" : str(ctx.content),
                    "author_name" : str(ctx.author.name),
                    "author_discriminator" : str(ctx.author.discriminator),
                    "time" : str(datetime.now())
                }
        filename = '/home/pi/discordbot/logs/message_logs/' + \
            str(math.floor(time.time()/86400))+'.json'
        try:
            with open(filename, 'r') as f:
                deletemessages = json.load(f)
                if str(ctx.guild.id) not in deletemessages.keys():
                    print("created guild dict")
                    deletemessages[str(ctx.guild.id)]={}
                if str(ctx.channel.id) not in deletemessages[str(ctx.guild.id)].keys():
                    print("created channel dict")
                    deletemessages[str(ctx.guild.id)][str(ctx.channel.id)] ={}
                
                deletemessages[str(ctx.guild.id)][str(ctx.channel.id)][str(ctx.id)] = jsonf
            with open(filename, 'w') as f:
                json.dump(deletemessages, f, indent=4)

        except:
            print("created file")
            with open(filename, 'w') as f:
                jsonfile = { str(ctx.guild.id) : {str(ctx.channel.id): {str(ctx.id) : jsonf}}}
                json.dump(jsonfile, f, indent=4)


  
    
def setup(bot):
    bot.add_cog(Base(bot))