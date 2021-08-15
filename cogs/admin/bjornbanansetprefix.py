
import json
import math
import re
import time

import discord
from discord.ext import commands


class Base(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    @commands.has_permissions(manage_guild=True)
    async def on_message(self, message):
        msg = message.content
        if msg[0:19] != "bjornbanansetprefix":
            return
        try:
            prefix = msg.split(" ")[1]
            prefixes = json.load(open('/tmp/discordbot/management/prefixes.json', 'r'))
            prefixes[str(message.guild.id)] = prefix
            json.dump(prefixes, open('/tmp/discordbot/management/prefixes.json', 'w'))
            print("new prefix", prefix)
        except:
            await message.channel.send('"You failed. "gsetprefix [prefix]"')


def setup(bot):
    bot.add_cog(Base(bot))
