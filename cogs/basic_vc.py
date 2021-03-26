import discord
import ffmpeg
from discord.ext import commands
from discord.utils import get
from enabledisable import checkenable


class Base(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def j(self,ctx):
        with open('/home/pi/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "j" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
            print(f"moved to a channel{channel}")
        else:
            voice = await channel.connect()
            print(f"connected to a channel{channel}")

        await ctx.send(f"Joined {channel}")


    @commands.command(pass_context=True)
    async def l(self,ctx):
        with open('/home/pi/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "l" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"Left {channel}")
            print(f"Left channel:{channel}")
        else:
            await ctx.send("Not in a channel f u")
            print(f"was asked to leave but not in channel{channel}")

    @commands.command(pass_context=True)
    async def od(self,ctx):
        with open('/home/pi/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "od" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return
        channel = ctx.message.author.voice.channel
        print(self.bot.voice_clients, ctx.guild)
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        path = r"/home/pi/discordbot/songs/djungeltrubbaduren.mp3"
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send("God has entered the chat")
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        vc.play(discord.FFmpegPCMAudio(path),
                after=lambda e: print("song is done"))
        vc.source = discord.PCMVolumeTransformer(vc.source)


    @commands.command(pass_context=True)
    async def erika(self,ctx):
        with open('/home/pi/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "erika" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        path = r"/home/pi/discordbot/songs/erika.mp3"
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send("God has entered the chat")
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        vc.play(discord.FFmpegPCMAudio(path),
                after=lambda e: print("song is done"))
        vc.source = discord.PCMVolumeTransformer(vc.source)
    
 

def setup(bot):
    bot.add_cog(Base(bot))




