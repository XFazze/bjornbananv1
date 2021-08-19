import discord, datetime, time
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import random


class Userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

 

# Userinfo
    
    @commands.command(pass_context=True, aliases= ['userinfo'])
    async def user(self, ctx, member:discord.Member = None):
        
        await ctx.message.delete()
        
        if member is None:
            
            roles_list = ' | '.join(map(str, ctx.author.roles))
            
            embed=discord.Embed(title=member, color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="ID", value=ctx.author.id, inline=False)
            embed.add_field(name="Nickname", value=ctx.author.nick, inline=False)
            embed.add_field(name="Highest role", value=ctx.author.top_role, inline=False)
            embed.add_field(name="Roles", value=roles_list, inline=False)
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        
        
        else:
            
            roles_list = ' | '.join(map(str, member.roles))
            
            embed=discord.Embed(title=member, color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="ID", value=member.id, inline=False)
            embed.add_field(name="Nickname", value=member.nick, inline=False)
            embed.add_field(name="Highest role", value=member.top_role, inline=False)
            embed.add_field(name="Roles", value=roles_list, inline=False)
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)
    
    
    @commands.command(pass_context=True, aliases=['av'])
    async def avatar(self, ctx, member:discord.Member = None):
        
        await ctx.message.delete()
        if member is None:
            
            embed=discord.Embed(title=ctx.author, color=random.randint(0, 0xFFFFFF))
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        
        
        else:
            
            embed=discord.Embed(title=member, color=random.randint(0, 0xFFFFFF))
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)
     
 

def setup(bot):
    bot.add_cog(Userinfo(bot))