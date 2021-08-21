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


class Serverinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

   
    
# Serverinfo
    @commands.command(pass_context=True, aliases=['serverinfo', 'guild'])
    async def server(self, ctx):
        await ctx.message.delete()
        
        
        embed=discord.Embed(title=ctx.guild, color=random.randint(0, 0xFFFFFF))
        embed.add_field(name="Owner", value=ctx.guild.owner, inline=False)
        embed.add_field(name="ID", value=ctx.guild.id, inline=False)
        embed.add_field(name="Member count", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Creation Date", value=ctx.guild.created_at, inline=False)
        embed.add_field(name="Region", value=ctx.guild.region, inline=False)
        embed.add_field(name="Number of text channels", value=len(ctx.guild.text_channels), inline=False)
        embed.add_field(name="Number of voice channels", value=len(ctx.guild.voice_channels), inline=False)
        embed.add_field(name="Number of categories", value=len(ctx.guild.categories), inline=False)
        
        
        embed.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
     

def setup(bot):
    bot.add_cog(Serverinfo(bot))