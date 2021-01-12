import discord
import json
import random
from gtts import gTTS
from discord.ext import commands
from discord.utils import get


class Base(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, aliases=['obi', '.quote'])
    async def quote_text(self,ctx):
        quote_list = json.load(open('/home/pi/discordbot/quote/quote.json'))
        quote_nr = random.randint(0, len(quote_list)-1)
        message = quote_list[quote_nr]["quote"] + \
            " - "+quote_list[quote_nr]["author"] + "_ _"
        sent = await ctx.send(message)
        # 👉, 👌, 😠
        emojis = ['\U0001f449', '\U0001f44C', '\U0001F620']
        for emoji in emojis:
            await sent.add_reaction(emoji)


    @commands.command(pass_context=True, aliases=['obiv', '.quote_voice'])
    async def quote_voice(self,ctx):
        quote_list = json.load(open('/home/pi/discordbot/quote/quote.json'))
        quote_nr = random.randint(0, len(quote_list)-1)
        message = "at your service"+"_ _"
        sent = await ctx.send(message)
        quote = quote_list[quote_nr]["quote"].replace('"', '')

        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        path = r"/home/pi/discordbot/quote/voice/"+quote+".mp3"
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send("God has entered the chat")
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        vc.play(discord.FFmpegPCMAudio(path),
                after=lambda e: print("song is done"))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        emojis = ['\U0001f449', '\U0001f44C', '\U0001F620']
        for emoji in emojis:
            await sent.add_reaction(emoji)


    @commands.command(pass_context=True, aliases=['add', '.quote_add'])
    async def quote_add(self,ctx):
        quote_org = ctx.message.content.split(' ', 1)
        quote = '"' + quote_org[1] + '"'
        if len(quote) > 200:
            print("tried to add too long")
            await ctx.send("Tha fuck, u trying to add a bible bitch??")
        author = ctx.message.author.name
        quote_list = json.load(open('/home/pi/discordbot/quote/quote.json'))
        for quote_storage in quote_list:
            if quote_storage["quote"] == quote:
                await ctx.send("U sleezy copyrighter")
                return
        new_quote = {"quote": quote, "author": author, "rating": 1}
        quote_list.append(new_quote)
        with open('/home/pi/discordbot/quote/quote.json', 'w') as file:
            json.dump(quote_list, file, indent=4)
        with open('/home/pi/discordbot/quote/all_quote.json', 'w') as file:
            json.dump(quote_list, file, indent=4)

        voice = gTTS(quote)
        filename = "/home/pi/discordbot/quote/voice/"+quote_org[1]+".mp3"
        voice.save(filename)

        message = "Added " + quote + " to the quote mind from " + author
        await ctx.send(message)


    def change(quote, amount):
        print("quote change", quote, amount)
        file = json.load(open('/home/pi/discordbot/quote/quote.json', 'r'))
        for quote_file in file:
            if quote_file["quote"] == quote:
                print("found quote")
                quote_file["rating"] += amount
                if quote_file["rating"] < -3:
                    print("remove gobi")
                    file.remove(quote_file)
                break
        with open('/home/pi/discordbot/quote/quote.json', 'w') as place:
            json.dump(file, place, indent=4)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        guild = self.bot.get_guild(payload.guild_id)
        if message.author == guild.get_member(self.bot.user.id) and "_ _" in message.content and payload.member != guild.get_member(self.bot.user.id):
            quote = message.content.split(" -")[0]
            quote = quote[:-3]
            if str(reaction) == "👉" or str(reaction) == "👌":
                change(quote, 1)
            if str(reaction) == "😠":
                change(quote, -1)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        guild = self.bot.get_guild(payload.guild_id)
        if message.author == guild.get_member(self.bot.user.id) and "_ _" in message.content and payload.member != guild.get_member(self.bot.user.id):
            quote = message.content.split(" -")[0]
            quote = quote[:-3]
            if str(reaction) == "👉" or str(reaction) == "👌":
                change(quote, -1)
            if str(reaction) == "😠":
                change(quote, 1)


def setup(bot):
    bot.add_cog(Base(bot))