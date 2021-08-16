import discord
import json
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
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def disable(self,ctx):
        try:
            command = str(ctx.message.content).split(" ")[1]
        except:
            await ctx.send("Provide a command")
        if command in ["enable", "disable"]:
            await ctx.send("cant disable this command")
        for botcommand in  self.bot.commands:
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

    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def enable(self,ctx):
        try:
            command = str(ctx.message.content).split(" ")[1]
        except:
            await ctx.send("Provide a command")
        if command in ["enable", "disable"]:
            await ctx.send("cant disable this command")
        for botcommand in  self.bot.commands:
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
        try:
            prefix = msg.split(" ")[1]
            prefixes = json.load(open('/tmp/discordbot/management/prefixes.json', 'r'))
            prefixes[str(message.guild.id)] = prefix
            json.dump(prefixes, open('/tmp/discordbot/management/prefixes.json', 'w'))
            print("new prefix", prefix)
            await message.channel.send('successfully changed the prefix')
        except:
            await message.channel.send('You failed. "bjornbanansetprefix [prefix]"')




    
    
    
    
    # Join roles

    @commands.command(pass_context=True, aliases=['jra', 'jradd'])
    @commands.has_permissions(manage_roles=True)
    async def joinroleadd(self, ctx):
        try:
            role_id = int(str(ctx.message.content).split(" ")[1][3:-1])
        except:
            await ctx.send("you forgot the role")
            return

        guild_id = ctx.message.guild.id
        with open('/tmp/discordbot/management/joinrole.json', 'r+') as f:
            joinrole = json.load(f)
            if str(guild_id) in joinrole.keys():
                if role_id in joinrole[str(guild_id)]:
                    await ctx.send("This channel is already added to joinrole")
                else:
                    joinrole[str(guild_id)].append(role_id)
                    await ctx.send("Added channel to joinrole")
                    with open('/tmp/discordbot/management/joinrole.json', 'w') as file:
                        json.dump(joinrole, file, indent=4)
            else:
                joinrole[int(guild_id)] = [role_id]
                await ctx.send("Added channel to joinrole")
                with open('/tmp/discordbot/management/joinrole.json', 'w') as file:
                    json.dump(joinrole, file, indent=4)


    @commands.command(pass_context=True, aliases=['jrr', 'jrremove'])
    @commands.has_permissions(manage_roles=True)
    async def joinroleremove(self, ctx):
        try:
            role_id = int(str(ctx.message.content).split(" ")[1][3:-1])
        except:
            await ctx.send("you forgot the role")
            return

        guild_id = ctx.message.guild.id
        with open('/tmp/discordbot/management/joinrole.json', 'r+') as f:
            joinrole = json.load(f)
            if str(guild_id) in joinrole.keys():
                print("exist")
                if role_id in joinrole[str(guild_id)]:
                    if len(joinrole[str(guild_id)]) > 1:
                        joinrole[str(guild_id)].remove(role_id)
                        with open('/tmp/discordbot/management/joinrole.json', 'w') as file:
                            json.dump(joinrole, file, indent=4)
                    else:
                        del joinrole[str(guild_id)]
                        with open('/tmp/discordbot/management/joinrole.json', 'w') as file:
                            json.dump(joinrole, file, indent=4)
                    await ctx.send("This role is removed")
                else:
                    await ctx.send("Channel not added")
            else:
                await ctx.send("Channel not added")


    @commands.command(pass_context=True, aliases=['jrl', 'jrlist'])
    async def joinrolelist(self, ctx):
        guild = ctx.guild
        embed=discord.Embed(title="Join roles", color=0xFFF4E6)
        with open('/tmp/discordbot/management/joinrole.json', 'r+') as f:
            joinrole = json.load(f)
            if str(guild.id) in joinrole.keys():
                for role_id in joinrole[str(guild.id)]:
                    role = get(guild.roles, id=role_id)
                    embed.add_field(name=role.name, value="\u200b", inline=False)
            else:
                embed.add_field(name="Mission failed", value="There are no join roles on this server", inline=False)
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        with open('/tmp/discordbot/management/joinrole.json', 'r+') as f:
            joinrole = json.load(f)
            if str(guild.id) in joinrole.keys():
                for role_id in joinrole[str(guild.id)]:
                    role = get(guild.roles, id=role_id)
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