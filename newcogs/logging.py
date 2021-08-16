import discord
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import math
import datetime

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Action log
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        action = "admin abuse"

        if before.self_deaf != after.self_deaf:
            channel_id = before.channel.id
            if before.self_deaf:
                action = "unselfdeaf"
            elif after.self_deaf:
                action = "selfdeaf"

        elif before.self_mute != after.self_mute:
            channel_id = before.channel.id
            if before.self_mute:
                action = "unselfmute"
            elif after.self_mute:
                action = "selfmute"

        elif before.self_stream != after.self_stream:
            channel_id = before.channel.id
            if before.self_stream:
                action = "unselfstream"
            elif after.self_stream:
                action = "selfstream"

        elif not before.channel:
            channel_id = after.channel.id
            action = "connect"

        elif not after.channel:
            channel_id = before.channel.id
            action = "disconnect"

        elif after.channel != before.channel:
            channel_id = [after.channel.id, before.channel.id]
            action = "move"

        if action == "admin abuse":
            return

        filename = '/tmp/discordbot/logs/vc_logs/' + \
            str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time())+" " + action+" " +
                        str(channel_id) + " "+str(member) + "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time())+" " + action+" " +
                        str(channel_id) + " "+str(member) + "\n")


    @commands.Cog.listener()
    async def on_message(self, message):
        member = await message.guild.fetch_member(message.author.id)
        filename = '/tmp/discordbot/logs/tc_logs/' + \
            str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " send " + str(message.guild.id) + " " + str(
                    message.channel.id) + " "+str(message.id) + " " + str(member) + " " + "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " send " + str(message.guild.id) + " " + str(
                    message.channel.id) + " "+str(message.id) + " " + str(member) + " " + "\n")


    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        filename = '/tmp/discordbot/logs/tc_logs/' + \
            str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " delete " + str(payload.guild_id) + " " +
                        str(payload.channel_id) + " " + str(payload.message_id) + " " + "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " delete " + str(payload.guild_id) + " " +
                        str(payload.channel_id) + " " + str(payload.message_id) + " " + "\n")


    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        filename = '/tmp/discordbot/logs/tc_logs/' + \
            str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " edit " + str(payload.data["guild_id"]) + " " + str(payload.data["channel_id"]) + " " + str(
                    payload.data["id"]) + " " + str(payload.data["author"]["username"]) + "#" + str(payload.data["author"]["discriminator"]) + "\n")
        except:
            try:
                with open(filename, 'w') as f:
                    f.write(str(time.time()) + " edit " + str(payload.data["guild_id"]) + " " + str(payload.data["channel_id"]) + " " + str(
                        payload.data["id"]) + " " + str(payload.data["author"]["username"]) + "#" + str(payload.data["author"]["discriminator"]) + "\n")
            except:
                print("the strange thing happeneded in actionlog")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        filename = '/tmp/discordbot/logs/tc_logs/' + \
            str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " reactadd " + str(payload.guild_id) + " " + str(payload.channel_id) + " " + str(payload.message_id) +
                        " " + str(payload.member.name) + "#" + str(payload.member.discriminator) + " " + str(payload.emoji.name) + "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " reactadd " + str(payload.guild_id) + " " + str(payload.channel_id) + " " + str(payload.message_id) +
                        " " + str(payload.member.name) + "#" + str(payload.member.discriminator) + " " + str(payload.emoji.name) + "\n")


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        filename = '/tmp/discordbot/logs/tc_logs/' + \
            str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " reactremove " + str(payload.guild_id) + " " + str(payload.channel_id) +
                        " " + str(payload.message_id) + " " + str(member) + " " + str(payload.emoji.name) + "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " reactremove " + str(payload.guild_id) + " " + str(payload.channel_id) +
                        " " + str(payload.message_id) + " " + str(member) + " " + str(payload.emoji.name) + "\n")


    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        filename = '/tmp/discordbot/logs/tc_logs/' + \
            str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " typing " + str(channel.guild.id) +
                        " " + str(channel.id) + " " + str(user)+"\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " typing " + str(channel.guild.id) +
                        " " + str(channel.id) + " " + str(user)+"\n")
 

# Join/leave log
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        filename = '/tmp/discordbot/logs/joinleave_logs/' + \
            str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " join " + str(member) + " " + str(member.guild.id) + "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " join " + str(member) + " " + str(member.guild.id) + "\n")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        filename = '/tmp/discordbot/logs/joinleave_logs/' + \
            str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " leave " + str(member) + " " + str(member.guild.id) + "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " leave " + str(member) + " " + str(member.guild.id) +  "\n")

   
# Message log
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        jsonf = {
                    "content" : str(ctx.content),
                    "author_name" : str(ctx.author.name),
                    "author_discriminator" : str(ctx.author.discriminator),
                    "time" : str(datetime.now())
                }
        filename = '/tmp/discordbot/logs/message_logs/' + \
            str(math.floor(time.time()/86400))+'.json'
        try:
            with open(filename, 'r') as f:
                deletemessages = json.load(f)
                if str(ctx.guild.id) not in deletemessages.keys():
                    deletemessages[str(ctx.guild.id)]={}
                if str(ctx.channel.id) not in deletemessages[str(ctx.guild.id)].keys():
                    deletemessages[str(ctx.guild.id)][str(ctx.channel.id)] ={}
                
                deletemessages[str(ctx.guild.id)][str(ctx.channel.id)][str(ctx.id)] = jsonf
            with open(filename, 'w') as f:
                json.dump(deletemessages, f, indent=4)

        except:
            print("created file")
            with open(filename, 'w') as f:
                jsonfile = { str(ctx.guild.id) : {str(ctx.channel.id): {str(ctx.id) : jsonf}}}
                json.dump(jsonfile, f, indent=4)


def setup(bot):
    bot.add_cog(Logging(bot))