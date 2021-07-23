import discord
import json
import os
import time
import copy
from datetime import datetime
from discord import embeds
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def e(self, ctx):
        message = ctx.message.content.split(" ")
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        if len(message) == 1:
            embed = discord.Embed(title="editd message")
            with open('/tmp/discordbot/logs/delete_logs/edit_mega.json', 'r') as f:
                edit_logs = json.load(f)
                if guild_id in edit_logs.keys():
                    if channel_id in edit_logs[guild_id].keys():
                        ret_message = {
                            "content": "The bot is broken send help",
                            "author_name": "Bj\u00f6rnbanan",
                            "author_discriminator": "6641",
                            "time": "1021-05-20 15:38:31.421036"
                        }
                        for key in edit_logs[guild_id][channel_id].keys():
                            if datetime.strptime(edit_logs[guild_id][channel_id][key]["time"], '%Y-%m-%d %H:%M:%S.%f') > datetime.strptime(ret_message["time"], '%Y-%m-%d %H:%M:%S.%f'):
                                ret_message = edit_logs[guild_id][channel_id][key]

                        embed.add_field(name=ret_message['time']+" from "+ret_message['author_name'] +
                                        "#"+ret_message['author_discriminator'], value=ret_message['content'])
                    else:
                        print("channel not found")
                        ret_message = "There are no editd messages"
                else:
                    print("guild not found")
                    ret_message = "There are no editd messages"
            await ctx.send(embed=embed)
        else:
            list = False
            index = 0
            mindex = 0
            for argument in message[1:]:
                print(argument)
                if "#" in argument:
                    pass

                if "list" in argument:
                    list = True
                if "-" in argument:
                    mindex = argument.split('-')

                try:
                    index = int(argument)
                except:
                    pass

            with open('/tmp/discordbot/logs/delete_logs/edit_mega.json', 'r') as f:
                edit_logs = json.load(f)
                if guild_id in edit_logs.keys():
                    temp_edit_logs = copy.deepcopy(edit_logs[guild_id])
                    if channel_id in temp_edit_logs.keys():
                        temp_edit_logs = temp_edit_logs[channel_id]
                        for key in temp_edit_logs.keys():
                            temp_edit_logs[key]['time'] = datetime.strptime(
                                temp_edit_logs[key]['time'], '%Y-%m-%d %H:%M:%S.%f').timestamp()
                        temp_edit_logs = sorted(
                            temp_edit_logs, key=lambda x: temp_edit_logs[x]['time'], reverse=True)
                        if list:
                            if int(index) == 0:
                                x = 0
                                embed = discord.Embed(title="editd Messages")
                                if 20 > len(temp_edit_logs):
                                    for message in temp_edit_logs:
                                        embed.add_field(value=edit_logs[guild_id][channel_id][message]["time"] + " from " + edit_logs[guild_id][channel_id][message]["author_name"] +
                                                        "#"+edit_logs[guild_id][channel_id][message]['author_discriminator'], name=str(x), inline=False)
                                        x += 1
                                else:
                                    for message in temp_edit_logs[:20]:
                                        embed.add_field(value=edit_logs[guild_id][channel_id][message]["time"] + " from " + edit_logs[guild_id][channel_id][message]["author_name"] +
                                                        "#"+edit_logs[guild_id][channel_id][message]['author_discriminator'], name=str(x), inline=False)
                                        x += 1
                                    embed.add_field(value="add a number to access the page",
                                                    name="page 0 of "+str(round(len(temp_edit_logs)/20)))
                                await ctx.send(embed=embed)

                            elif index > round(len(temp_edit_logs)/20):
                                embed = discord.Embed(
                                    title="There arent that many pages")
                                await ctx.send(embed=embed)

                            else:
                                embed = discord.Embed(title="editd Messages")
                                i1 = int(index)*20
                                i2 = int(index)*20+20
                                x = i1
                                for message in temp_edit_logs[i1:i2]:
                                    embed.add_field(value=edit_logs[guild_id][channel_id][message]["time"] + " from " + edit_logs[guild_id][channel_id][message]["author_name"] +
                                                    "#"+edit_logs[guild_id][channel_id][message]['author_discriminator'], name=str(x), inline=False)
                                    x += 1
                                embed.add_field(value="add a number to access the page", name="page " + str(
                                    index) + " of "+str(round(len(temp_edit_logs)/20)))
                                await ctx.send(embed=embed)

                        elif type(index) == int and type(mindex) == int:
                            if int(argument) > len(temp_edit_logs):
                                embed = discord.Embed(
                                    title="Look help command")
                                await ctx.send(embed=embed)
                                return
                            else:
                                message = edit_logs[guild_id][channel_id][temp_edit_logs[int(
                                    argument)]]
                                embed = discord.Embed(
                                    title="editd message nr" + argument)
                                embed.add_field(name=message['time']+" from "+message["author_name"] +
                                                "#"+message['author_discriminator'], value=message['content'])
                                await ctx.send(embed=embed)
                                return

                        elif mindex:
                            try:
                                mindex[0] = int(mindex[0])
                                mindex[1] = int(mindex[1])
                            except:
                                embed = discord.Embed(
                                    title="Look help command")
                                await ctx.send(embed=embed)
                                return

                            if mindex[1]-mindex[0] > 20:
                                embed = discord.Embed(
                                    title="Look help command")
                                await ctx.send(embed=embed)
                                return

                            elif mindex[1] > len(temp_edit_logs):
                                embed = discord.Embed(
                                    title="Look help command")
                                await ctx.send(embed=embed)
                                return

                            else:
                                embed = discord.Embed(title="editd Messages")
                                for i in range(1+mindex[1]-mindex[0]):
                                    message = edit_logs[guild_id][channel_id][temp_edit_logs[i+mindex[0]]]
                                    embed.add_field(name="nr " + str(i+mindex[0]) + " at " + message['time']+" from "+message["author_name"] +
                                                    "#"+message['author_discriminator'], value=message['content'], inline=False)
                                await ctx.send(embed=embed)

                        # embed.add_field(name=ret_message['time']+" from "+ret_message['author_name']+"#"+ret_message['author_discriminator'], value=ret_message['content'])
                    else:
                        print("channel not found")
                        ret_message = "There are no editd messages"
                else:
                    print("guild not found")
                    ret_message = "There are no editd messages"

    '''
        with open('/tmp/discordbot/logs/edit_logs/edit_mega.json', 'r') as f:
            edit_logs = json.load(f)
            sending_message = 'editd messages in this channel\n'
            for message in edit_logs[str(ctx.guild.id)][str(ctx.channel.id)]:
                sending_message = sending_message +"\n" + edit_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]["time"] + " " + edit_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['author_name'] + "#" + edit_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['author_discriminator']  + ":\n" + edit_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['content']
            sending_message = "```" + sending_message + "```"
            await ctx.send(sending_message)
    '''

    @commands.Cog.listener()
    async def on_raw_message_edit(self, ctx):
        print("edited message")
        filepath = '/tmp/discordbot/logs/message_logs/'
        for file in os.listdir(filepath):
            filename = "/tmp/discordbot/logs/message_logs/" + file
            with open(filename, 'r') as f:
                messagelog = json.load(f)
                try:
                    message = messagelog[str(ctx.guild_id)][str(
                        ctx.channel_id)][str(ctx.message_id)]
                    print("got here")
                    break
                except:
                    pass
        print("yes me", message)
        try:
            if message:
                if message["author_name"] == "Bj\u00f6rnbanan" or message["author_name"] == "Bj\u00f6rnbanan_experimental":
                    print("worked")
                    return
                pass
        except:
            return
        print("hello ther")
        with open('/tmp/discordbot/logs/delete_logs/edit_mega.json', 'r') as f:
            edit_logs = json.load(f)
            if str(ctx.guild_id) not in edit_logs.keys():
                print("created guild dict")
                edit_logs[str(ctx.guild_id)] = {}
            if str(ctx.channel_id) not in edit_logs[str(ctx.guild_id)].keys():
                print("created channel dict")
                edit_logs[str(ctx.guild_id)][str(ctx.channel_id)] = {}

            edit_logs[str(ctx.guild_id)][str(ctx.channel_id)
                                           ][str(ctx.message_id)] = message
            with open('/tmp/discordbot/logs/edit_logs/edit_mega.json', 'w') as file:
                print("success")
                json.dump(edit_logs, file, indent=4)


def setup(bot):
    bot.add_cog(Base(bot))
