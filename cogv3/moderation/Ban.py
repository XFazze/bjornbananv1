import discord
from ..admin.managecommands import perms
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


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Ban

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.check(perms)
    async def ban(self, ctx, member:discord.Member = None, *reason):
        
        # Sets default reason if not specified
        if not reason:
            reason = "Reason was not specified"
        
        # Bans member if the author has a higher role than the subject.
        if member is None:
            await ctx.send("Please mention someone to ban")
        
        else:
            
            if ctx.author.top_role.position > member.top_role.position:
                
                reason = ' '.join(map(str, reason))
                await ctx.send(f'{member} was banned with reason "{reason}"')
                await ctx.guild.ban(member, reason=reason)
                
            else:
                await ctx.send("The person you are trying to ban is more powerful than you")
    

# Ban list

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.check(perms)
    async def banlist(self, ctx):
        
        await ctx.message.delete()
        
        banlist = await ctx.guild.bans()
        
        for i in range(0, len(banlist)):
            
            embed=discord.Embed(title="Banned member", color=0xff0000)
            embed.add_field(name="User", value=banlist[i].user, inline=False)
            embed.add_field(name="ID", value=banlist[i].user.id, inline=False)
            embed.add_field(name="Reason", value=banlist[i].reason, inline=False)
            await ctx.send(embed=embed)


# Unban

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.check(perms)
    async def unban(self, ctx, member = None):

        # Unbans a member
        if member is None:
            await ctx.send("Please mention someone to unban")
        
        else:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")
            
            for ban_entry in banned_users:
                user = ban_entry.user
                
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'{user} was unbanned')



def setup(bot):
    bot.add_cog(Ban(bot))