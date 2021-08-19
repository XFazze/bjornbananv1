import discord
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import math
import random
import re
import asyncio


class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

   
  
# To-Do

    @commands.command(pass_context=True)
    async def todo(self, ctx):
        await ctx.message.delete()
        id = random.randint(100, 999)
        embed = discord.Embed(title="Todo #"+str(id), description=str(id), color=discord.colour.Color.blue())
        await ctx.send(embed=embed)
        embed = discord.Embed(title="Active #"+str(id), description=str(id), color=discord.colour.Color.red())
        await ctx.send(embed=embed)
        embed = discord.Embed(title="Done #"+str(id), description=str(id), color=discord.colour.Color.green())
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def tadd(self, ctx, *content):
        await ctx.message.delete()
        try:
            id = int(content[0])
        except:
            await ctx.send("you need to include the id for the lis")
            return
        if len(content[0]) != 3:
            await ctx.send("the id of the list is 4 digits")
            return
        found = False
        async for message in ctx.channel.history(limit=111):
            if len(message.embeds) == 1:
                try:
                    if id == int(message.embeds[0].description) and message.embeds[0].title[0:4] == "Todo":
                        found = True
                        break
                except:
                    pass
        if not found:
            await ctx.send("wrong id")
            return
        if len(content) < 2:
            await ctx.send("you need to write the activity you want")
            return
            
        print(dir(message.embeds[0]))
        embed = message.embeds[0]
        newmessage = ""
        for word in content[1:]:
            newmessage = newmessage+" " +word

        embed.add_field(name=str(len(embed.fields)+1), value=newmessage, inline=False)
        await message.edit(embed=embed)
        
        
    @commands.command(pass_context=True, aliases=['ta'])
    async def tactive(self, ctx, *content):
        await ctx.message.delete()
        try:
            id = int(content[0])
        except:
            await ctx.send("you need to include the id for the list")
            return
        if len(content[0]) != 3:
            await ctx.send("the id of the list is 3 digits")
            return
        found = False
        async for message in ctx.channel.history(limit=111):
            if len(message.embeds) == 1:
                try:
                    if id == int(message.embeds[0].description) and message.embeds[0].title[0:4] == "Todo":
                        found = True
                        break
                except:
                    pass
        if not found:
            await ctx.send("wrong id")
            return

        
            
        embed = message.embeds[0]
        try:
            index = int(content[1])-1
            field = embed.fields[index]
        except:
            await ctx.send("the index is out of range")
            return
        
        embed.remove_field(index)
        await message.edit(embed=embed)

        async for message in ctx.channel.history(limit=111):
            if len(message.embeds) == 1:
                try:
                    if id == int(message.embeds[0].description) and message.embeds[0].title[0:4] == "Acti":
                        break
                except:
                    pass

        embed = message.embeds[0]
        embed.add_field(name=str(len(message.embeds[0].fields)+1), value=field.value, inline=False)
        await message.edit(embed=embed)


    @commands.command(pass_context=True, aliases=['td'])
    async def tdone(self, ctx, *content):
        await ctx.message.delete()
        try:
            id = int(content[0])
        except:
            await ctx.send("you need to include the id for the list")
            return
        if len(content[0]) != 3:
            await ctx.send("the id of the list is 4 digits")
            return
        found = False
        async for message in ctx.channel.history(limit=111):
            if len(message.embeds) == 1:
                try:
                    if id == int(message.embeds[0].description) and message.embeds[0].title[0:4] == "Acti":
                        found = True
                        break
                except:
                    pass
        if not found:
            await ctx.send("wrong id")
            return

        try:
            index = int(content[1])-1
        except:
            await ctx.send("the index is out of range")
            return
            
        embed = message.embeds[0]
        print(embed.fields[index])
        field = embed.fields[index]
        embed.remove_field(index)
        await message.edit(embed=embed)

        async for message in ctx.channel.history(limit=111):
            if len(message.embeds) == 1:
                try:
                    if id == int(message.embeds[0].description) and message.embeds[0].title[0:4] == "Done":
                        break
                except:
                    pass

        embed = message.embeds[0]
        embed.add_field(name=str(len(message.embeds[0].fields)+1), value=field.value, inline=False)
        await message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Todo(bot))