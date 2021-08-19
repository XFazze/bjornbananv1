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


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




# Kick

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member, *reason):
        # Sets default reason if not specified
        if not reason:
            reason = "Reason was not specified"
        
        # Bans member if the author has a higher role than the subject.
        if member is None:
            await ctx.send("Please mention someone to kick")
        
        else:
            
            if ctx.author.top_role.position > member.top_role.position:
                
                reason = ' '.join(map(str, reason))
                await ctx.send(f'{member} was kicked with reason "{reason}"')
                await ctx.guild.kick(member, reason=reason)
                
            else:
                await ctx.send("The person you are trying to kick is more powerful than you")



def setup(bot):
    bot.add_cog(Kick(bot))