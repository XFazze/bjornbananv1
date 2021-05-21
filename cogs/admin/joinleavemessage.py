import discord
import json
import time
import os
from discord.ext import commands

# how many times a user has been here
class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def ej(self, ctx):
        await ctx.message.delete()
        with open('/home/pi/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            if str(ctx.guild.id) in joinleavemessage.keys():
                if ctx.channel.id in joinleavemessage[str(ctx.guild.id)]:
                    await ctx.send("This channel is already added to joinleavemessage")
                else:
                    joinleavemessage[str(ctx.guild.id)].append(ctx.channel.id)
                    await ctx.send("Added channel to joinleavemessage")
                    with open('/home/pi/discordbot/management/joinleavemessage.json', 'w') as file:
                        json.dump(joinleavemessage, file, indent=4)
            else:
                joinleavemessage[str(ctx.guild.id)] = [ctx.channel.id]
                await ctx.send("Added channel to joinleavemessage")
                with open('/home/pi/discordbot/management/joinleavemessage.json', 'w') as file:
                    json.dump(joinleavemessage, file, indent=4)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def dj(self, ctx):
        await ctx.message.delete()
        with open('/home/pi/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            if str(ctx.guild.id) in  joinleavemessage.keys():
                if ctx.channel.id in joinleavemessage[str(ctx.guild.id)]:
                    joinleavemessage[str(ctx.guild.id)].remove(ctx.channel.id)
                    await ctx.send("removed channel from joinleavemessage")
                    with open('/home/pi/discordbot/management/joinleavemessage.json', 'w') as file:
                        json.dump(joinleavemessage, file, indent=4)
                    return
            await ctx.send("Channel not in joinleavemessage")


        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('/home/pi/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            directory = os.fsencode('/home/pi/discordbot/logs/joinleave_logs/')
            times = 0
            for file in os.listdir(directory):
                filename = '/home/pi/discordbot/logs/joinleave_logs/'+os.fsdecode(file)
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
        with open('/home/pi/discordbot/management/joinleavemessage.json', 'r+') as f:
            joinleavemessage = json.load(f)
            directory = os.fsencode('/home/pi/discordbot/logs/joinleave_logs/')
            times = 0
            for file in os.listdir(directory):
                filename = '/home/pi/discordbot/logs/joinleave_logs/'+os.fsdecode(file)
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

def setup(bot):
    bot.add_cog(Base(bot))