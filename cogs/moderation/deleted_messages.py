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

    @commands.command(pass_context=True, aliases=['d', 'deleted', 'snipe'])
    async def deletedmessages(self, ctx):
        message = ctx.message.content.split(" ")
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        if len(message) == 1:
            embed = discord.Embed(title="Deleted message")
            with open('/tmp/discordbot/logs/delete_logs/delete_mega.json', 'r') as f:
                delete_logs = json.load(f)
                if guild_id in delete_logs.keys():
                    if channel_id in delete_logs[guild_id].keys():
                        ret_message = {
                            "content": "The bot is broken send help",
                            "author_name": "Bj\u00f6rnbanan",
                            "author_discriminator": "6641",
                            "time": "1021-05-20 15:38:31.421036"
                        }
                        for key in delete_logs[guild_id][channel_id].keys():
                            if datetime.strptime(delete_logs[guild_id][channel_id][key]["time"], '%Y-%m-%d %H:%M:%S.%f') > datetime.strptime(ret_message["time"], '%Y-%m-%d %H:%M:%S.%f'):
                                ret_message = delete_logs[guild_id][channel_id][key]

                        embed.add_field(name=ret_message['time']+" from "+ret_message['author_name'] +
                                        "#"+ret_message['author_discriminator'], value=ret_message['content'])
                    else:
                        print("channel not found")
                        ret_message = "There are no deleted messages"
                else:
                    print("guild not found")
                    ret_message = "There are no deleted messages"
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

            with open('/tmp/discordbot/logs/delete_logs/delete_mega.json', 'r') as f:
                delete_logs = json.load(f)
                if guild_id in delete_logs.keys():
                    temp_delete_logs = copy.deepcopy(delete_logs[guild_id])
                    if channel_id in temp_delete_logs.keys():
                        temp_delete_logs = temp_delete_logs[channel_id]
                        for key in temp_delete_logs.keys():
                            temp_delete_logs[key]['time'] = datetime.strptime(
                                temp_delete_logs[key]['time'], '%Y-%m-%d %H:%M:%S.%f').timestamp()
                        temp_delete_logs = sorted(
                            temp_delete_logs, key=lambda x: temp_delete_logs[x]['time'], reverse=True)
                        if list:
                            if int(index) == 0:
                                x = 0
                                embed = discord.Embed(title="Deleted Messages")
                                if 20 > len(temp_delete_logs):
                                    for message in temp_delete_logs:
                                        embed.add_field(value=delete_logs[guild_id][channel_id][message]["time"] + " from " + delete_logs[guild_id][channel_id][message]["author_name"] +
                                                        "#"+delete_logs[guild_id][channel_id][message]['author_discriminator'], name=str(x), inline=False)
                                        x += 1
                                else:
                                    for message in temp_delete_logs[:20]:
                                        embed.add_field(value=delete_logs[guild_id][channel_id][message]["time"] + " from " + delete_logs[guild_id][channel_id][message]["author_name"] +
                                                        "#"+delete_logs[guild_id][channel_id][message]['author_discriminator'], name=str(x), inline=False)
                                        x += 1
                                    embed.add_field(value="add a number to access the page",
                                                    name="page 0 of "+str(round(len(temp_delete_logs)/20)))
                                await ctx.send(embed=embed)

                            elif index > round(len(temp_delete_logs)/20):
                                embed = discord.Embed(
                                    title="There arent that many pages")
                                await ctx.send(embed=embed)

                            else:
                                embed = discord.Embed(title="Deleted Messages")
                                i1 = int(index)*20
                                i2 = int(index)*20+20
                                x = i1
                                for message in temp_delete_logs[i1:i2]:
                                    embed.add_field(value=delete_logs[guild_id][channel_id][message]["time"] + " from " + delete_logs[guild_id][channel_id][message]["author_name"] +
                                                    "#"+delete_logs[guild_id][channel_id][message]['author_discriminator'], name=str(x), inline=False)
                                    x += 1
                                embed.add_field(value="add a number to access the page", name="page " + str(
                                    index) + " of "+str(round(len(temp_delete_logs)/20)))
                                await ctx.send(embed=embed)

                        elif type(index) == int and type(mindex) == int:
                            if int(argument) > len(temp_delete_logs):
                                embed = discord.Embed(
                                    title="Look help command")
                                await ctx.send(embed=embed)
                                return
                            else:
                                message = delete_logs[guild_id][channel_id][temp_delete_logs[int(
                                    argument)]]
                                embed = discord.Embed(
                                    title="Deleted message nr" + argument)
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

                            elif mindex[1] > len(temp_delete_logs):
                                embed = discord.Embed(
                                    title="Look help command")
                                await ctx.send(embed=embed)
                                return

                            else:
                                embed = discord.Embed(title="Deleted Messages")
                                for i in range(1+mindex[1]-mindex[0]):
                                    message = delete_logs[guild_id][channel_id][temp_delete_logs[i+mindex[0]]]
                                    embed.add_field(name="nr " + str(i+mindex[0]) + " at " + message['time']+" from "+message["author_name"] +
                                                    "#"+message['author_discriminator'], value=message['content'], inline=False)
                                await ctx.send(embed=embed)

                        # embed.add_field(name=ret_message['time']+" from "+ret_message['author_name']+"#"+ret_message['author_discriminator'], value=ret_message['content'])
                    else:
                        print("channel not found")
                        ret_message = "There are no deleted messages"
                else:
                    print("guild not found")
                    ret_message = "There are no deleted messages"

    '''
        with open('/tmp/discordbot/logs/delete_logs/delete_mega.json', 'r') as f:
            delete_logs = json.load(f)
            sending_message = 'Deleted messages in this channel\n'
            for message in delete_logs[str(ctx.guild.id)][str(ctx.channel.id)]:
                sending_message = sending_message +"\n" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]["time"] + " " + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['author_name'] + "#" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['author_discriminator']  + ":\n" + delete_logs[str(ctx.guild.id)][str(ctx.channel.id)][message]['content']
            sending_message = "```" + sending_message + "```"
            await ctx.send(sending_message)
    '''

    @commands.Cog.listener()
    async def on_raw_message_delete(self, ctx):
        filepath = '/tmp/discordbot/logs/message_logs/'
        for file in os.listdir(filepath):
            filename = "/tmp/discordbot/logs/message_logs/" + file
            with open(filename, 'r') as f:
                messagelog = json.load(f)
                try:
                    message = messagelog[str(ctx.guild_id)][str(
                        ctx.channel_id)][str(ctx.message_id)]
                    break
                except:
                    pass
        try:
            if message:
                if message["author_name"] == "Bj\u00f6rnbanan" or message["author_name"] == "Bj\u00f6rnbanan_experimental":
                    print("worked")
                    return
                pass
        except:
            return
        with open('/tmp/discordbot/logs/delete_logs/delete_mega.json', 'r') as f:
            delete_logs = json.load(f)
            if str(ctx.guild_id) not in delete_logs.keys():
                delete_logs[str(ctx.guild_id)] = {}
            if str(ctx.channel_id) not in delete_logs[str(ctx.guild_id)].keys():
                delete_logs[str(ctx.guild_id)][str(ctx.channel_id)] = {}

            delete_logs[str(ctx.guild_id)][str(ctx.channel_id)
                                           ][str(ctx.message_id)] = message
            with open('/tmp/discordbot/logs/delete_logs/delete_mega.json', 'w') as file:
                json.dump(delete_logs, file, indent=4)


def setup(bot):
    bot.add_cog(Base(bot))
