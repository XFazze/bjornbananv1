import discord
from ..admin.managecommands import perms
from discord.utils import get
from discord.ext import commands
from gtts import gTTS

class textToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Basic VC

    @commands.command(pass_context=True, aliases=['tts'])
    @commands.check(perms)
    async def texttospeech(self,ctx, *, message):
        if len(message) < 0:
            await ctx.reply("Use your words")
            return

        if len(message) > 50:
            await ctx.reply("Tha fuck, u trying to bible bitch??")
            return
        voice = gTTS(message)
        path = "/home/pi/discordbot/static/tts/"+message+".mp3"
        voice.save(path)
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
    bot.add_cog(textToSpeech(bot))
