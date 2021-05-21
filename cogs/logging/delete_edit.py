import discord
import json
import time
import os
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def d(self, ctx):
        with open('/home/pi/discordbot/logs/delete_logs/delete_mega.json', 'r') as f:
            delete_logs = json.load(f)
            sending_message = 'Deleted messages in this channel\n'
            for message in delete_logs[str(ctx.guild.id)][str(ctx.channel.id)]:
                sending_message = sending_message +"\n" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]["time"] + " " + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['author_name'] + "#" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['author_discriminator']  + ":\n" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['content']
            sending_message = "```" + sending_message + "```"
            await ctx.send(sending_message)

    @commands.command(pass_context=True)
    async def e(self, ctx):
        with open('/home/pi/discordbot/logs/delete_logs/edit_mega.json', 'r') as f:
            delete_logs = json.load(f)
            sending_message = 'Edited messages in this channel\n'
            for message in delete_logs[str(ctx.guild.id)][str(ctx.channel.id)]:
                sending_message = sending_message +"\n" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]["time"] + " " + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['author_name'] + "#" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['author_discriminator']  + ":\n" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['content']
            sending_message = "```" + sending_message + "```"
            await ctx.send(sending_message)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, ctx):
        filepath = '/home/pi/discordbot/logs/message_logs/'
        for file in os.listdir(filepath):
            filename = "/home/pi/discordbot/logs/message_logs/" + file
            with open(filename, 'r') as f:
                messagelog = json.load(f)
                try:
                    message = messagelog[str(ctx.guild_id)][str(ctx.channel_id)][str(ctx.message_id)]
                    break
                except:
                    pass
        try:
            if message:
                pass
        except:
            return
        with open('/home/pi/discordbot/logs/delete_logs/delete_mega.json', 'r') as f:
            delete_logs = json.load(f)
            if str(ctx.guild_id) not in delete_logs.keys():
                print("created guild dict")
                delete_logs[str(ctx.guild_id)] = {}
            if str(ctx.channel_id) not in delete_logs[str(ctx.guild_id)].keys():
                print("created channel dict")
                delete_logs[str(ctx.guild_id)][str(ctx.channel_id)] = {}
                
            delete_logs[str(ctx.guild_id)][str(ctx.channel_id)][str(ctx.message_id)] = message
            with open('/home/pi/discordbot/logs/delete_logs/delete_mega.json', 'w') as file:
                json.dump(delete_logs, file, indent=4)
                
    @commands.Cog.listener()
    async def on_raw_message_edit(self, ctx):
        filepath = '/home/pi/discordbot/logs/message_logs/'
        for file in os.listdir(filepath):
            filename = "/home/pi/discordbot/logs/message_logs/" + file
            with open(filename, 'r') as f:
                messagelog = json.load(f)
                try:
                    message = messagelog[str(ctx.data['guild_id'])][str(ctx.channel_id)][str(ctx.message_id)]
                    break
                except:
                    pass
        try:
            if message:
                pass
        except:
            return
        with open('/home/pi/discordbot/logs/delete_logs/edit_mega.json', 'r') as f:
            delete_logs = json.load(f)
            if str(ctx.data['guild_id']) not in delete_logs.keys():
                print("created guild dict")
                delete_logs[str(ctx.data['guild_id'])] = {}
            if str(ctx.channel_id) not in delete_logs[str(ctx.data['guild_id'])].keys():
                print("created channel dict")
                delete_logs[str(ctx.data['guild_id'])][str(ctx.channel_id)] = {}
                
            delete_logs[str(ctx.data['guild_id'])][str(ctx.channel_id)][str(ctx.message_id)] = message
            with open('/home/pi/discordbot/logs/delete_logs/edit_mega.json', 'w') as file:
                json.dump(delete_logs, file, indent=4)
        pass
        

def setup(bot):
    bot.add_cog(Base(bot))