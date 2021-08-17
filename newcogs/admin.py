import discord
import json
from discord import member
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Enable/disable command

    @commands.command(pass_context=True, enabled=False)
    @commands.has_permissions(manage_roles=True)
    async def adisable(self, ctx):
        try:
            command = str(ctx.message.content).split(" ")[1]
        except:
            await ctx.send("Provide a command")
        if command in ["enable", "disable"]:
            await ctx.send("cant disable this command")
        for botcommand in self.bot.commands:
            if command == str(botcommand):
                guild_id = ctx.guild.id
                with open('/tmp/discordbot/management/enable.json', 'r+') as f:
                    enable = json.load(f)
                    if str(guild_id) in enable.keys():
                        if command in enable[str(guild_id)]:
                            await ctx.send("This command is already disabled")
                        else:
                            enable[str(guild_id)].append(command)
                            await ctx.send("Disabled command")
                            with open('/tmp/discordbot/management/enable.json', 'w') as file:
                                json.dump(enable, file, indent=4)
                    else:
                        enable[int(guild_id)] = [command]
                        await ctx.send("Disabled command")
                        with open('/tmp/discordbot/management/enable.json', 'w') as file:
                            json.dump(enable, file, indent=4)

    @commands.command(pass_context=True, enabled=False)
    @commands.has_permissions(manage_roles=True)
    async def aenable(self, ctx):
        try:
            command = str(ctx.message.content).split(" ")[1]
        except:
            await ctx.send("Provide a command")
        if command in ["enable", "disable"]:
            await ctx.send("cant disable this command")
        for botcommand in self.bot.commands:
            if command == str(botcommand):
                guild_id = ctx.guild.id
                with open('/tmp/discordbot/management/enable.json', 'r+') as f:
                    enable = json.load(f)
                    if str(guild_id) in enable.keys():
                        print("exist")
                        if command in enable[str(guild_id)]:
                            if len(enable[str(guild_id)]) > 1:
                                enable[str(guild_id)].remove(command)
                                with open('/tmp/discordbot/management/enable.json', 'w') as file:
                                    json.dump(enable, file, indent=4)
                            else:
                                del enable[str(guild_id)]
                                with open('/tmp/discordbot/management/enable.json', 'w') as file:
                                    json.dump(enable, file, indent=4)
                            await ctx.send("This command is enabled")
                            return
                        else:
                            await ctx.send("Command already allowed")
                            return
                    else:
                        await ctx.send("Command already allowed")
                        return
        await ctx.send("Command does not exist")

# Björnbanan set prefix

    @commands.Cog.listener()
    @commands.has_permissions(manage_guild=True)
    async def on_message(self, message):
        msg = message.content
        if msg[0:19] != "bjornbanansetprefix":
            return
        if len(msg.split(' ')) != 2:
            embed = discord.Embed(
                title="Prove a valid prefix. bjornbanansetprefix [prefix]", color=0xFD3333)
            await message.channel.send(embed=embed)
            return

        prefix = msg.split(' ')[1]

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": message.guild.id}
        config = collection.find_one(myquery)["config"]

        config["prefix"] = prefix
        newvalue = {"$set": {"config": config}}
        collection.update_one(myquery, newvalue)
        embed = discord.Embed(
            title="Successfully changed the prefix to " + prefix, color=0x00FF42)
        await message.channel.send(embed=embed)

# Join roles

    @commands.command(pass_context=True, aliases=['jra', 'jradd'])
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

# Reaction roles

    @commands.command(pass_context=True, aliases=['r'])
    @commands.has_permissions(manage_roles=True)
    async def reactionroles(self, ctx):
        try:
            role_id = int(str(ctx.message.content).split(" ")[1][3:-1])
        except:
            await ctx.send("you forgot the role variable, format: grear @role emoji text. OBS spaces")
            return
        try:
            emoji = str(ctx.message.content).split(" ")[2]
        except:
            await ctx.send("you forgot the amoji variable, format: grear @role emoji text. OBS spaces")
            return
        try:
            text = str(ctx.message.content).split(" ")[3:]
        except:
            await ctx.send("you forgot the text variable, format: grear @role emoji text. OBS spaces")
            return
        highest_role = ctx.message.author.roles[-1]
        role = get(ctx.guild.roles, id=role_id)
        for roles in ctx.guild.roles:
            if role == roles:
                break
            elif highest_role == roles:
                return
        phrase = ""
        for word in text:
            phrase = phrase+" "+word
        message = "Role: "+str(role) + " |" + phrase

        bot_message = await ctx.send(message)
        await bot_message.add_reaction(emoji)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(
            message.reactions, emoji=payload.emoji.name)
        guild = self.bot.get_guild(payload.guild_id)
        if message.author == guild.get_member(self.bot.user.id) and "Role:" == str(message.content)[0:5] and payload.member != guild.get_member(self.bot.user.id):
            role = str(message.content)[6:].split(" |")[0]
            role = discord.utils.get(guild.roles, name=role)
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(
            message.reactions, emoji=payload.emoji.name)
        guild = self.bot.get_guild(payload.guild_id)
        if message.author == guild.get_member(self.bot.user.id) and "Role:" == str(message.content)[0:5]:
            role = str(message.content)[6:].split(" |")[0]
            role = discord.utils.get(guild.roles, name=role)
            member = await guild.fetch_member(payload.user_id)
            await member.remove_roles(role)

    @commands.command(pass_context=True, aliases=['c'])
    async def reactionrolesclean(self, ctx):
        await ctx.message.delete()
        channel = ctx.message.channel
        messages = await channel.history(limit=200).flatten()
        tosend = []
        for message in messages:
            if message.content[0:6] == "Role: " and message.author == ctx.guild.get_member(self.bot.user.id) and message.reactions != []:
                tosend.insert(0, {"content": message.content,
                                  "reaction": message.reactions[0]})
                await message.delete()
        for sending in tosend:
            msg = await ctx.send(sending["content"])
            await msg.add_reaction(sending["reaction"])


def setup(bot):
    bot.add_cog(Admin(bot))
