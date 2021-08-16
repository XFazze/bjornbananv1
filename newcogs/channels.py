import discord
import json
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
from discord.utils import get
import time
import os
import pymongo as pm







class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cleanse.start()
        self.hidechannels.start()
        






    # Delete pinned

    @commands.command(pass_context=True, aliases=['edp'])
    @commands.has_permissions(manage_messages=True)
    async def enabledeletepinned(self, ctx):
        with open('/tmp/discordbot/management/delete_pinned.json', 'r+') as f:
            delete_pinned = json.load(f)
            c_id = ctx.channel.id
            if c_id in delete_pinned:
                await ctx.send("This channel is already added to delete_pinned")
            else:
                delete_pinned.append(c_id)
                await ctx.send("Added channel to delete_pinned")
                with open('/tmp/discordbot/management/delete_pinned.json', 'w') as file:
                    json.dump(delete_pinned, file, indent=4)


    @commands.command(pass_context=True, aliases=['ddp'])
    @commands.has_permissions(manage_messages=True)
    async def disabledeletepinned(self, ctx):
        with open('/tmp/discordbot/management/delete_pinned.json', 'r+') as f:
            delete_pinned = json.load(f)
            c_id = ctx.channel.id
            if c_id in delete_pinned:
                delete_pinned.remove(c_id)
                await ctx.send("removed channel from delete_pinned")
                with open('/tmp/discordbot/management/delete_pinned.json', 'w') as file:
                    json.dump(delete_pinned, file, indent=4)
            else:
                await ctx.send("This channel isnta a delete_pinned channel")


    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.type.value == 6:
            with open('/tmp/discordbot/management/delete_pinned.json', 'r') as f:
                channels = json.load(f)
                for channel in channels:
                    if channel == ctx.channel.id:
                        await ctx.delete()








    # Deleting channel

    @commands.command(pass_context=True, aliases=['ed'])
    @commands.has_permissions(manage_messages=True)
    async def enabledelete(self, ctx):
        with open('/tmp/discordbot/management/deletingchannel.json', 'r+') as f:
            deletingchannel = json.load(f)
            c_id = ctx.channel.id
            if c_id in deletingchannel:
                await ctx.send("This channel is already added to deletingchannel")
            else:
                deletingchannel.append(c_id)
                await ctx.send("Added channel to deletingchannel")
                with open('/tmp/discordbot/management/deletingchannel.json', 'w') as file:
                    json.dump(deletingchannel, file, indent=4)


    @commands.command(pass_context=True, aliases=['dd'])
    @commands.has_permissions(manage_messages=True)
    async def disabledelete(self, ctx):
        with open('/tmp/discordbot/management/deletingchannel.json', 'r+') as f:
            deletingchannel = json.load(f)
            c_id = ctx.channel.id
            if c_id in deletingchannel:
                deletingchannel.remove(c_id)
                await ctx.send("removed channel from deletingchannel")
                with open('/tmp/discordbot/management/deletingchannel.json', 'w') as file:
                    json.dump(deletingchannel, file, indent=4)
            else:
                await ctx.send("This channel isnta a deletingchannel channel")


    @tasks.loop(seconds=10)
    async def cleanse(self):
        with open('/tmp/discordbot/management/deletingchannel.json', 'r') as f:
            deletingchannel = json.load(f)
            if deletingchannel:
                for channel in deletingchannel:
                    channel = self.deletingchannel.get_channel(channel)
                    messages = await channel.history(limit=100).flatten()
                    await channel.delete_messages(messages)


    @cleanse.before_loop
    async def before_cleanse(self):
        print('deletingchannel enabled')
        await self.cleanse.wait_until_ready()









    # Better vc

    @commands.command(pass_context=True, aliases=['eb'])
    @commands.has_permissions(manage_roles=True)
    async def enablebettervc(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]
        
        
        if ctx.author.voice.channel.category_id in config["bettervc"]:
            embed = discord.Embed(
                title="Category already decided, remove if changing", color=0xFD3333)
            await ctx.send(embed=embed)

        else:
            config["bettervc"].append(ctx.author.voice.channel.category_id)
            newvalue = {"$set": {"config": config}}
            collection.update_one(myquery, newvalue)
            embed = discord.Embed(
                title="Added category to bettervc", color=0x00FF42)
            await ctx.send(embed=embed)


    @commands.command(pass_context=True, aliases=['db'])
    @commands.has_permissions(manage_roles=True)
    async def disablebettervc(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        config = collection.find_one(myquery)["config"]

        if ctx.author.voice.channel.category_id in config["bettervc"]:
            config["bettervc"].remove(ctx.author.voice.channel.category_id)
            newvalue = {"$set": {"config": config}}
            collection.update_one(myquery, newvalue)
            embed = discord.Embed(
                title="Removing category from bettervc", color=0x00FF42)
            await ctx.send(embed=embed)
        else:
            await ctx.send("category isn't in bettervc")

    @tasks.loop(seconds=10)
    async def hidechannels(self):
        collection = MongoClient('localhost', 27017).maindb.guilds
        guilds = collection.find({})
        for guild in guilds:
            guild_object = self.bot.get_guild(guild["id"])
            if len(guild["config"]["bettervc"]) != 0:
                for category in guild["config"]["bettervc"]:
                    category_object = get(self.bot.get_all_channels(), id=category)
                    empty_channels = []
                    for channel in category_object.channels:
                        if len(channel.members) == 0:
                            empty_channels.append(channel)
                    empty_channels.pop(0)
                    for hiding_channel in empty_channels:
                        await hiding_channel.set_permissions(guild_object.default_role, read_messages=False)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        collection = MongoClient('localhost', 27017).maindb.guilds
        guilds = collection.find_one({"id" : after.channel.guild.id})
        guild_object = self.bot.get_guild(guilds["id"])
        if after.channel.category_id in guilds["config"]["bettervc"] and len(after.channel.members) == 1:
            category_object = get(self.bot.get_all_channels(), id=after.channel.category_id)
            for empty_channel in category_object.channels:
                if len(empty_channel.members) == 0:
                    await empty_channel.set_permissions(guild_object.default_role, read_messages=None)
                    break


    @hidechannels.before_loop
    async def before_hidechannels(self):
        await self.bot.wait_until_ready()








    # Join - Leave message

    @commands.command(pass_context=True, aliases=['ejlm'])
    @commands.has_permissions(manage_messages=True)
    async def enablejoinleavemessage(self, ctx):
        await ctx.message.delete()
        with open('/tmp/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            if str(ctx.guild.id) in joinleavemessage.keys():
                if ctx.channel.id in joinleavemessage[str(ctx.guild.id)]:
                    await ctx.send("This channel is already added to joinleavemessage")
                else:
                    joinleavemessage[str(ctx.guild.id)].append(ctx.channel.id)
                    await ctx.send("Added channel to joinleavemessage")
                    with open('/tmp/discordbot/management/joinleavemessage.json', 'w') as file:
                        json.dump(joinleavemessage, file, indent=4)
            else:
                joinleavemessage[str(ctx.guild.id)] = [ctx.channel.id]
                await ctx.send("Added channel to joinleavemessage")
                with open('/tmp/discordbot/management/joinleavemessage.json', 'w') as file:
                    json.dump(joinleavemessage, file, indent=4)


    @commands.command(pass_context=True, aliases=['djlm'])
    @commands.has_permissions(manage_messages=True)
    async def disablejoinleavemessage(self, ctx):
        await ctx.message.delete()
        with open('/tmp/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            if str(ctx.guild.id) in  joinleavemessage.keys():
                if ctx.channel.id in joinleavemessage[str(ctx.guild.id)]:
                    joinleavemessage[str(ctx.guild.id)].remove(ctx.channel.id)
                    await ctx.send("removed channel from joinleavemessage")
                    with open('/tmp/discordbot/management/joinleavemessage.json', 'w') as file:
                        json.dump(joinleavemessage, file, indent=4)
                    return
            await ctx.send("Channel not in joinleavemessage")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('/tmp/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            directory = os.fsencode('/tmp/discordbot/logs/joinleave_logs/')
            times = 0
            for file in os.listdir(directory):
                filename = '/tmp/discordbot/logs/joinleave_logs/'+os.fsdecode(file)
                with open(filename, 'r') as file:
                    filelines = file.readlines()
                    for line in filelines:
                        if "join" in line and str(member) in line:
                            times += 1


            if str(member.guild.id) in joinleavemessage.keys():
                for channel in joinleavemessage[str(member.guild.id)]:
                    channel = self.bot.get_channel(channel)
                    embed = discord.Embed(title=str(member)+ "  joined " + str(times)+" times" , description=time.asctime() , color=0x00ff00)
                    await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open('/tmp/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            directory = os.fsencode('/tmp/discordbot/logs/joinleave_logs/')
            times = 0
            for file in os.listdir(directory):
                filename = '/tmp/discordbot/logs/joinleave_logs/'+os.fsdecode(file)
                with open(filename, 'r') as file:
                    filelines = file.readlines()
                    for line in filelines:
                        if "leave" in line and str(member) in line:
                            times += 1
                
            if str(member.guild.id) in joinleavemessage.keys():
                for channel in joinleavemessage[str(member.guild.id)]:
                    channel = self.bot.get_channel(channel)
                    embed = discord.Embed(title=str(member) + "  left " + str(times)+" times", description=time.asctime(), color=0xFF0000)
                    await channel.send(embed=embed)








    # Role log

    @commands.command(pass_context=True, aliases=['er'])
    @commands.has_permissions(manage_roles=True)
    async def enablerolelog(self, ctx):
        with open('/tmp/discordbot/management/rolelog.json', 'r+') as f:
            rolelog = json.load(f)
            c_id = ctx.channel.id
            g_id = str(ctx.guild.id)
            if c_id in rolelog.values():
                await ctx.send("This channel is already added to rolelog")
            else:
                rolelog[g_id] = c_id
                await ctx.send("Added channel to rolelog")
                with open('/tmp/discordbot/management/rolelog.json', 'w') as file:
                    json.dump(rolelog, file, indent=4)
    
    
    @commands.command(pass_context=True, aliases=['dr'])
    @commands.has_permissions(manage_roles=True)
    async def disablerolelog(self, ctx):
        with open('/tmp/discordbot/management/rolelog.json', 'r+') as f:
            rolelog = json.load(f)
            c_id = ctx.channel.id
            g_id = str(ctx.guild.id)
            if c_id in rolelog.values():
                del rolelog[g_id]
                await ctx.send("removed channel to rolelog")
                with open('/tmp/discordbot/management/rolelog.json', 'w') as file:
                    json.dump(rolelog, file, indent=4)
            else:
                await ctx.send("This channel isnta a rolelog channel")
    
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles == after.roles:
            return
        else:
            with open('/tmp/discordbot/management/rolelog.json', 'r') as f:
                rolelog = json.load(f)
                guild_id = str(before.guild.id)
                if guild_id not in rolelog.keys():
                    return
                channel_id = rolelog[guild_id]
                channel = self.bot.get_channel(channel_id)
                if len(before.roles) > len(after.roles):
                    role = list(set(before.roles)-set(after.roles))[0]
                    message = "User: "+ str(before) +"\nRole removed: " +role.name
                    await channel.send(message)
                else:
                    role = list(set(after.roles)-set(before.roles))[0]
                    if role.id == 802300001875001455:
                        message = "@everyone User: "+ str(before) +"\nRole added: " +role.name
                    else:
                        message = "User: "+ str(before) +"\nRole added: " +role.name
                    await channel.send(message)






















def setup(bot):
    bot.add_cog(Channels(bot))