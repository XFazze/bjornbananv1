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


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Bomb reactions
    @commands.command(pass_context=True, aliases=['boom', 'bomb', 'reactions'])
    async def bomb_reactions(self, ctx, *id):
        emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '☺', '😊', '😇', '🙂', '🙃',
                    '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐',
                    '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹',  '😣',
                    '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱',
                    '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯',
                    '😦', '😧', '😮', '😲', '🤤', '😪', '😵', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒',
                    '🤕', '🤑', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠', '️', '👽', '👾',
                    '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
        await ctx.message.delete()
        if len(id) == 0:
            async for mess in ctx.message.channel.history(limit=1):
                for i in range(20):
                    emoji = emojis[random.randint(0, len(emojis)-1)]
                    await mess.add_reaction(emoji)
        else:
            try:
                print(id)
                mess = await ctx.fetch_message(int(id[0]))
                for i in range(20):
                    emoji = emojis[random.randint(0, len(emojis)-1)]
                    await mess.add_reaction(emoji)
            except:
                await ctx.send("not a valid id")


# Clear   
    @commands.command(aliases = ['purge','delete'], usage="clear [int]")
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = None):
        with self.bot.typing():
            if amount == None:
                embed = discord.Embed(title=f'Usage: `{self.bot.get_command("clear").usage}`')
                await ctx.send(embed=embed)
            else:
                try:
                    amount = int(amount)
                    await ctx.channel.purge(limit=amount+1)
                    embed = discord.Embed(title=f'Tried to delete `{amount}` messages')
                    await ctx.send(embed=embed)
                except:
                    embed = discord.Embed(title=f'Usage: `{self.bot.get_command("clear").usage}`')
                    await ctx.send(embed=embed)
                

# Color code 
    @commands.command(pass_context=True, aliases=['cc'])
    async def colorcode(self, ctx):
        await ctx.message.delete()
        for role in ctx.message.author.roles:
            if str(role)[0] == ";":
                if len(str(ctx.message.content).split(" ")) > 1:
                    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', "#"+str(ctx.message.content).split(" ")[1]):
                        await role.edit(color=int(("0x"+str(ctx.message.content).split(" ")[1]), 16), reason="Testing")
                        await ctx.send("Successfully changed Color of your role")
                        return
                    else:
                        await ctx.send("Colorcode is invalid format:gcolor ffffff")
                        return
                else:
                    await ctx.send("You need to provide a color code like this:gcolor ffffff")
                    return
        await ctx.send("You dont have a role. \nSo I will create a role for you:")
        role_name = ";"+str(ctx.message.author)[0:-5]
        await ctx.send(role_name)
        role = await ctx.guild.create_role(name=role_name)
        await ctx.message.author.add_roles(role)
        await ctx.send("I have also given you the roles you're welcume")
    
    
# DND  
    @commands.Cog.listener()
    async def on_message(self, message):
        msg=message.content
        try:
            if msg[0] != "d":
                return
        except:
            return
        try:
            for sym in msg[1:]:
                if sym in "+-*/":
                    pass
                else:
                    p = int(sym)
            new = []
            temp = ""
            for symbol in msg:
                try:
                    x = int(symbol)
                    temp = temp+symbol
                except:
                    new.append(temp)
                    new.append(symbol)
                    temp = ""
            new.append(temp)
            dice = int(new[2])
            new[0] = random.randint(1, dice)
            new[1:]=new[3:]
            x = 1
            value = []
            operator=[]
            for i in new:
                x = x*-1
                if x < 0:
                    value.append(i)
                else:
                    operator.append(i)


            result = value[0]
            for op in operator:
                x = operator.index(op)
                if op == "+":
                    result = result+int(value[x+1])
                if op == "-":
                    result = result-int(value[x+1])
                if op == "/":
                    result = result/int(value[x+1])
                if op == "*":
                    result = result*int(value[x+1])
            print(f"success  {value[0]} {result}")
            await message.channel.send(f"```d{dice}:{value[0]} = {result}```")
        except:
            return


    @commands.command(pass_context=True, aliases=['df'])
    @commands.has_permissions(manage_channels=True)
    async def dndframer(self, ctx):
        try:
            name = ctx.message.content[11:].split(",")[0]
        except:
            await ctx.send('format was wrong("gdndframer your name @person1 @person2")')
        guild = ctx.guild
        role = await guild.create_role(name=name)
        dm = ctx.message.author
        players = ctx.message.mentions
        await dm.add_roles(role)

        category = await guild.create_category(name)
        await category.set_permissions(guild.default_role, read_messages=False)
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = True
        await category.set_permissions(role, overwrite=overwrite)
        for player in players:
            await player.add_roles(role)
            channel_perm = await guild.create_text_channel(name=player.display_name+" dm", category=category)
            await channel_perm.set_permissions(role, read_messages=False)
            await channel_perm.set_permissions(dm, overwrite=overwrite)
            await channel_perm.set_permissions(player, overwrite=overwrite)

        channels = [name, "dice", "viktigt", "kartor", "stats", "initiative"]
        vc_channels = ["talk", "hjälp av dm"]
        dm_channels = ["dice-dm", "endast-dm", "hp-dm"]
        for channel in channels:
            await guild.create_text_channel(name=channel, category=category)
        for channel in vc_channels:
            await guild.create_voice_channel(name=channel, category=category)
        for channel in dm_channels:
            channel_perm = await guild.create_text_channel(name=channel, category=category)
            await channel_perm.set_permissions(role, read_messages=False)
            await channel_perm.set_permissions(dm, overwrite=overwrite)
    
  
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
    bot.add_cog(Utilities(bot))