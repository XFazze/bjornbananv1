import discord
import json
import ffmpeg

from discord.utils import get
from discord.ext import commands
from enabledisable import checkenable


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def tsbotadd(self, ctx):
        with open('/home/pi/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "tsbotadd" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return
        with open('/home/pi/discordbot/management/tsbot.json', 'r+') as f:
            tsbot = json.load(f)
        c_id = ctx.author.voice.channel.id
        if c_id == None:
            await ctx.send("Join a channel twat")
        if c_id in tsbot:
            await ctx.send("This channel is already added to tsbot")
        else:
            tsbot.append(c_id)
            await ctx.send("Added channel to tsbot")
            with open('/home/pi/discordbot/management/tsbot.json', 'w') as file:
                json.dump(tsbot, file, indent=4)
    
    @commands.command(pass_context=True)
    async def tsbotremove(self, ctx):
        with open('/home/pi/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "tsbotremove" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return
        with open('/home/pi/discordbot/management/tsbot.json', 'r+') as f:
            tsbot = json.load(f)
            c_id = ctx.author.voice.channel.id
            if c_id in tsbot:
                tsbot.remove(c_id)
                await ctx.send("removed channel from tsbot")
                with open('/home/pi/discordbot/management/tsbot.json', 'w') as file:
                    json.dump(tsbot, file, indent=4)
            else:
                await ctx.send("This channel isnta a tsbot channel")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        with open('/home/pi/discordbot/management/tsbot.json', 'r+') as f:
            tsbot = json.load(f)
        if after.channel != None:
            channel_id = after.channel.id
        else:
            channel_id = " bajs"
        '''
        if before.self_deaf != after.self_deaf:
            channel_id = before.channel.id
            if channel_id in tsbot:
                if before.self_deaf:
                    print("unselfdeaf")
                elif after.self_deaf:
                    print( "selfdeaf")

        elif before.self_mute != after.self_mute:
            channel_id = before.channel.id
            if channel_id in tsbot:
                if before.self_mute:
                    print("unselfmute")
                elif after.self_mute:
                    print("selfmute")


        elif before.self_stream != after.self_stream:
            channel_id = before.channel.id
            if channel_id in tsbot:
                if before.self_stream:
                    print("unselfstream")
                elif after.self_stream:
                    print("selfstream")
        
    
        '''


        if channel_id in tsbot:
            path = "/home/pi/discordbot/songs/ts3join.mp3"
            print("connect")
            channel = after.channel
            guild = member.guild
            voice = get(self.bot.voice_clients, guild=guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                await channel.connect()
                print("connect")
            vc = get(self.bot.voice_clients, guild=guild)
            vc.play(discord.FFmpegPCMAudio(path),
                    after=lambda e: print("song is done"))
            vc.source = discord.PCMVolumeTransformer(vc.source)

        elif before.channel.id in tsbot:
            print("disconnect") 
        


def setup(bot):
    bot.add_cog(Base(bot))