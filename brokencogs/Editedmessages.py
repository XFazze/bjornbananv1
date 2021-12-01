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


class Editedmessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Editedmessages

    @commands.command(pass_context=True, aliases = ['e'])
    @commands.check(perms)
    async def editedmessages(self, ctx):
        
        await ctx.message.delete()
        with open('/tmp/discordbot/logs/delete_logs/edit_mega.json', 'r') as f:
            delete_logs = json.load(f)
            sending_message = 'Edited messages in this channel\n'
            for message in delete_logs[str(ctx.guild.id)][str(ctx.channel.id)]:
                sending_message = sending_message + "\n" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]["time"] + " " + delete_logs[str(ctx.guild.id)][str(
                    ctx.channel.id)][message]['author_name'] + "#" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['author_discriminator'] + ":\n" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['content']
            sending_message = "```" + sending_message + "```"
            await ctx.reply(sending_message)


    @commands.Cog.listener()
    async def on_raw_message_edit(self, ctx):
        filepath = '/tmp/discordbot/logs/message_logs/'
        for file in os.listdir(filepath):
            filename = "/tmp/discordbot/logs/message_logs/" + file
            with open(filename, 'r') as f:
                messagelog = json.load(f)
                try:
                    message = messagelog[str(ctx.data['guild_id'])][str(
                        ctx.channel_id)][str(ctx.message_id)]
                    break
                except:
                    pass
        try:
            if message:
                pass
        except:
            return
        with open('/tmp/discordbot/logs/delete_logs/edit_mega.json', 'r') as f:
            delete_logs = json.load(f)
            if str(ctx.data['guild_id']) not in delete_logs.keys():
                delete_logs[str(ctx.data['guild_id'])] = {}
            if str(ctx.channel_id) not in delete_logs[str(ctx.data['guild_id'])].keys():
                delete_logs[str(ctx.data['guild_id'])
                            ][str(ctx.channel_id)] = {}

            delete_logs[str(ctx.data['guild_id'])][str(
                ctx.channel_id)][str(ctx.message_id)] = message
            with open('/tmp/discordbot/logs/delete_logs/edit_mega.json', 'w') as file:
                json.dump(delete_logs, file, indent=4)
        pass



def setup(bot):
    bot.add_cog(Editedmessages(bot))