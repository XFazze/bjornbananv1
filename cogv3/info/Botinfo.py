import discord, datetime, time
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import random


class Botinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Botinfo
    @commands.command(pass_context=True, aliases=['botinfo', 'bot'])
    async def appinfo(self, ctx):
        res = await self.bot.application_info()
        embed=discord.Embed(title=res.name, description=res.description, color=0x00FF42)
        if res.bot_public:
            embed.add_field(name="Public bot Owner:", value=res.owner.name+"#"+res.owner.discriminator)
        else:
            embed.add_field(name="Private bot Owner: ", value=res.owner.name+"#"+res.owner.discriminator)
        embed.add_field(name='Id', value=res.id, inline=False)
        embed.add_field(name='Guilds', value=len(self.bot.guilds), inline=False)
        embed.add_field(name='Users', value=len(self.bot.users), inline=False)
        embed.add_field(name='Commands', value=len(self.bot.commands), inline=False)
        embed.add_field(name='Emojis', value=len(self.bot.emojis), inline=False)
        embed.add_field(name='Latency', value=round(self.bot.latency*10000)*0.1, inline=False)
        embed.add_field(name='Private channels', value=len(self.bot.private_channels), inline=False)
        embed.add_field(name='Voice clients', value=len(self.bot.voice_clients), inline=False)
        await ctx.send(embed=embed)

        

def setup(bot):
    bot.add_cog(Botinfo(bot))