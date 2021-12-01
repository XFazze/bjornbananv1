import discord
from ..admin.managecommands import perms
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import ffmpeg
from gtts import gTTS


class Basicvc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
# Basic VC
    @commands.command(pass_context=True, aliases=['j'])
    @commands.check(perms)
    async def join(self,ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
            print(f"moved to a channel{channel}")
        else:
            voice = await channel.connect()
            print(f"connected to a channel{channel}")

        await ctx.reply(f"Joined {channel}")


    @commands.command(pass_context=True, aliases=['l'])
    @commands.check(perms)
    async def leave(self,ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
            await ctx.reply(f"Left {voice.channel}")
        else:
            await ctx.reply("Not in a channel f u")


    @commands.command(pass_context=True)
    @commands.check(perms)
    async def od(self,ctx):
        channel = ctx.message.author.voice.channel
        print(self.bot.voice_clients, ctx.guild)
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        path = r"/home/pi/discordbot/songs/djungeltrubbaduren.mp3"
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.reply("God has entered the chat")
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        vc.play(discord.FFmpegPCMAudio(path),
                after=lambda e: print("song is done"))
        vc.source = discord.PCMVolumeTransformer(vc.source)


    @commands.command(pass_context=True)
    @commands.check(perms)
    async def erika(self,ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        path = r"/tmp/discordbot/songs/erika.mp3"
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.reply("God has entered the chat")
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        vc.play(discord.FFmpegPCMAudio(path),
                after=lambda e: print("song is done"))
        vc.source = discord.PCMVolumeTransformer(vc.source)


    @commands.command(pass_context=True, aliases=['tts'])
    @commands.check(perms)
    async def texttospeech(self,ctx):
        message = ctx.message.content[6:]
        if len(message) > 50:
            print("tried to add too long")
            await ctx.reply("Tha fuck, u trying to bible bitch??")
            return
        voice = gTTS(message)
        filename = "/tmp/discordbot/quote/tts/"+message+".mp3"
        voice.save(filename)
        path=filename
        
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.reply("God has entered the chat")
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        vc.play(discord.FFmpegPCMAudio(path),
                after=lambda e: print("song is done"))
        vc.source = discord.PCMVolumeTransformer(vc.source)


def setup(bot):
    bot.add_cog(Basicvc(bot))
