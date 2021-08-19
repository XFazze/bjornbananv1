import discord
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import asyncio
import random
import datetime
import copy


class Tempban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Tempban
    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def tempban(self, ctx, member:discord.Member = None, days = None, *reason):
        # Sets default time and reason if not specified
        if days is None:
            days = 7
            
        if reason is None:
            reason = "Reason was not specified"
        
        
        # Bans member for the specified time if a member is mentioned and if the author has a higher role than the subject.
        if member is None:
            await ctx.send("Please mention someone to ban")
        
        
        else:
            
            if ctx.author.top_role.position > member.top_role.position:
                
                reason = ' '.join(map(str, reason))
                
                t = int(days)*24*60*60
                
                await ctx.send(f'{member} was banned with reason "{reason}" for {int(t/60/60/24)} days')
                    
                await ctx.guild.ban(member, reason=reason)
                
                await asyncio.sleep(t)
                await member.unban()
                
            
            else:
                await ctx.send("The person you are trying to ban is more powerful than you")



def setup(bot):
    bot.add_cog(Tempban(bot))