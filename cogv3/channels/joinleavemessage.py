import discord
from ..admin.managecommands import perms
import json
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
from discord.utils import get
import time
import os
import pymongo as pm


class joinleavemessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# joinleavemessage 

    @commands.command(pass_context=True, aliases=['ejlm'])
    @commands.has_permissions(manage_messages=True)
    @commands.check(perms)
    async def enablejoinleavemessage(self, ctx):
        await ctx.message.delete()
        with open('/tmp/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            if str(ctx.guild.id) in joinleavemessage.keys():
                if ctx.channel.id in joinleavemessage[str(ctx.guild.id)]:
                    await ctx.reply("This channel is already added to joinleavemessage")
                else:
                    joinleavemessage[str(ctx.guild.id)].append(ctx.channel.id)
                    await ctx.reply("Added channel to joinleavemessage")
                    with open('/tmp/discordbot/management/joinleavemessage.json', 'w') as file:
                        json.dump(joinleavemessage, file, indent=4)
            else:
                joinleavemessage[str(ctx.guild.id)] = [ctx.channel.id]
                await ctx.reply("Added channel to joinleavemessage")
                with open('/tmp/discordbot/management/joinleavemessage.json', 'w') as file:
                    json.dump(joinleavemessage, file, indent=4)

    @commands.command(pass_context=True, aliases=['djlm'])
    @commands.has_permissions(manage_messages=True)
    @commands.check(perms)
    async def disablejoinleavemessage(self, ctx):
        await ctx.message.delete()
        with open('/tmp/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            if str(ctx.guild.id) in joinleavemessage.keys():
                if ctx.channel.id in joinleavemessage[str(ctx.guild.id)]:
                    joinleavemessage[str(ctx.guild.id)].remove(ctx.channel.id)
                    await ctx.reply("removed channel from joinleavemessage")
                    with open('/tmp/discordbot/management/joinleavemessage.json', 'w') as file:
                        json.dump(joinleavemessage, file, indent=4)
                    return
            await ctx.reply("Channel not in joinleavemessage")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('/tmp/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            directory = os.fsencode('/tmp/discordbot/logs/joinleave_logs/')
            times = 0
            for file in os.listdir(directory):
                filename = '/tmp/discordbot/logs/joinleave_logs/' + \
                    os.fsdecode(file)
                with open(filename, 'r') as file:
                    filelines = file.readlines()
                    for line in filelines:
                        if "join" in line and str(member) in line:
                            times += 1

            if str(member.guild.id) in joinleavemessage.keys():
                for channel in joinleavemessage[str(member.guild.id)]:
                    channel = self.bot.get_channel(channel)
                    embed = discord.Embed(title=str(
                        member) + "  joined " + str(times)+" times", description=time.asctime(), color=0x00ff00)
                    await channel.reply(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open('/tmp/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            directory = os.fsencode('/tmp/discordbot/logs/joinleave_logs/')
            times = 0
            for file in os.listdir(directory):
                filename = '/tmp/discordbot/logs/joinleave_logs/' + \
                    os.fsdecode(file)
                with open(filename, 'r') as file:
                    filelines = file.readlines()
                    for line in filelines:
                        if "leave" in line and str(member) in line:
                            times += 1

            if str(member.guild.id) in joinleavemessage.keys():
                for channel in joinleavemessage[str(member.guild.id)]:
                    channel = self.bot.get_channel(channel)
                    embed = discord.Embed(title=str(
                        member) + "  left " + str(times)+" times", description=time.asctime(), color=0xFF0000)
                    await channel.reply(embed=embed)


def setup(bot):
    bot.add_cog(joinleavemessage(bot))
