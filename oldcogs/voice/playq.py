import discord
import ffmpeg
import youtube_dl
import os
import json
import time
from os import system
from discord.utils import get
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio

class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.musiccleanse.start()


    @commands.command(pass_context=True)
    async def play(self,ctx, url: str):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        song_there = os.path.isfile("songs/song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music end or use the 'stop' command")
            return
        await ctx.send("im doing this for you")
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        print("1")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("2")
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')
        print("3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        voice.volume = 100
        voice.is_playing()

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"Left {channel}")
        else:
            await ctx.send("YOure a hoe")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def musicadd(self, ctx):
        with open('/tmp/discordbot/management/music.json', 'r+') as f:
            music = json.load(f)
            c_id = ctx.channel.id
            if c_id in music:
                await ctx.send("This channel is already added to music")
                print("tried to add music but alreaddy added added")
            else:
                music.append(c_id)
                await ctx.send("Added channel to music")
                print("enabled music")
                with open('/tmp/discordbot/management/music.json', 'w') as file:
                    json.dump(music, file, indent=4)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def musicremove(self, ctx):
        with open('/tmp/discordbot/management/music.json', 'r+') as f:
            music = json.load(f)
            c_id = ctx.channel.id
            if c_id in music:
                music.remove(c_id)
                await ctx.send("removed channel from music")
                print("disabled music")
                with open('/tmp/discordbot/management/music.json', 'w') as file:
                    json.dump(music, file, indent=4)
            else:
                await ctx.send("This channel isnta a music channel")
                print("tried to remove music but wasnt added")

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('/tmp/discordbot/management/music.json', 'r') as f:
            music = json.load(f)
            if message.channel.id not in music or message.author == self.bot.user:
                return
        channel = message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=message.author.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        song_there = os.path.isfile("songs/song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await message.channel.send("Wait for the current playing music end or use the 'stop' command")
            return
        mymessage = await message.channel.send("im doing this for you")
        voice = get(self.bot.voice_clients, guild=message.author.guild)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        url = message.content
        print(url)
        print("1")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("2")
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')
        print("3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        voice.volume = 100
        voice.is_playing()

    @tasks.loop(seconds=360)
    async def musiccleanse(self):
        with open('/tmp/discordbot/management/music.json', 'r') as f:
            music = json.load(f)
            if music:
                for channel in music:
                    channel = self.bot.get_channel(channel)
                    messages = await channel.history(limit=100).flatten()
                    for msg in messages:
                        if msg.author == self.bot.user and msg.content[0] == "?":
                            print("yikess")

                    await channel.delete_messages(messages)
    
    @musiccleanse.before_loop
    async def before_musiccleanse(self):
        print('musiccleanse enabled')
        await self.bot.wait_until_ready()





def setup(bot):
    bot.add_cog(Base(bot))