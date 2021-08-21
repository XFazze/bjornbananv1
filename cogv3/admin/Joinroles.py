from cogv3.admin.managecommands import managecommands
import discord
from managecommands import perms
import json
from discord import member
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm


class Joinroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



# Join roles

    @commands.command(pass_context=True, aliases=['jra', 'jradd'])
    @commands.check(perms)
    @commands.has_permissions(manage_roles=True)
    async def joinroleadd(self, ctx, role: discord.Role = None):
        if role == None:
            embed = discord.Embed(title="Provide a role", color=0xFD3333)
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            await ctx.send(embed=discord.Embed(title="You dont have the permissions to add this role", color=0xFD3333))
            return

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]

        if role.id in config["joinrole"]:
            await ctx.send(embed=discord.Embed(title="This role is already added to joinrole", color=0xFD3333))
            return
        else:
            config["joinrole"].append(role.id)
            await ctx.send(embed=discord.Embed(title="Added role to joinrole", color=0x00FF42))

        newvalue = {"$set": {"config": config}}
        collection.update_one(myquery, newvalue)

    @commands.command(pass_context=True, aliases=['jrr', 'jrremove'])
    @commands.check(perms)
    @commands.has_permissions(manage_roles=True)
    async def joinroleremove(self, ctx, role: discord.Role = None):
        if role == None:
            embed = discord.Embed(title="Provide a role", color=0xFD3333)
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            await ctx.send(embed=discord.Embed(title="You dont have the permissions to remve this role", color=0xFD3333))
            return

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]

        if role.id in config["joinrole"]:
            config["joinrole"].remove(role.id)
            await ctx.send(embed=discord.Embed(title="Role removed from joinrole", color=0x00FF42))
        else:
            await ctx.send(embed=discord.Embed(title="Role not in joinrole", color=0xFD3333))
            return

        newvalue = {"$set": {"config": config}}
        collection.update_one(myquery, newvalue)

    @commands.command(pass_context=True, aliases=['jrl', 'jrlist'])
    @commands.check(perms)
    async def joinrolelist(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]
        if len(config["joinrole"]) != 0:
            embed = discord.Embed(title="Join roles", color=0xFFF4E6)
            for role_id in config["joinrole"]:
                role = get(ctx.guild.roles, id=role_id)
                embed.add_field(
                    name=role.name, value="\u200b", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=discord.Embed(title="There are no join roles on this server", color=0xFD3333))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": member.guild.id}
        config = collection.find_one(myquery)["config"]
        if len(config["joinrole"]) != 0:
            for role_id in config["joinrole"]:
                role = get(member.guild.roles, id=role_id)
                print(role)
                await member.add_roles(role)



def setup(bot):
    bot.add_cog(Joinroles(bot))
