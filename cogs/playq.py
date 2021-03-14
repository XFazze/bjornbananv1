import discord
import ffmpeg
from discord.utils import get
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def play(self,ctx):
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
def setup(bot):
    bot.add_cog(Base(bot))