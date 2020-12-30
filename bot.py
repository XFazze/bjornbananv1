import discord
import time
import os
import datetime
import audioread
import random
import json
import ffmpeg
from discord.ext import commands
from discord.utils import get
from codemy import code

intents = discord.Intents.default()
intents.members = True
bot_prefix = 'g'
bot = commands.Bot(command_prefix=bot_prefix, Intents=intents)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "n")
    await bot.change_presence(activity=discord.Game(name="you | ghelp"))

# upvote/downvote
'''
1. check if bot sent message
2. check if bot sent reaction
3. check if it's a "_ _" in the message
4. check which emoji
5. write
'\U0001f449','\U0001f44C', '\U0001F620'
'''

def change(quote, amount):
    print("quote change", quote, amount)
    file = json.load(open('/home/pi/discordbot/quote.json', 'r'))
    for quote_file in file:
        if quote_file["quote"] == quote:
            quote_file["rating"] += amount
            if quote_file["rating"] < -3:
                print("remove gobi")
                file.remove(quote_file)
            break
    with open('/home/pi/discordbot/quote.json', 'w') as place:
        json.dump(file, place, indent=4)



@bot.event
async def on_raw_reaction_add(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    if str(message.author) == "Björnbanan#6641" and "_ _" in message.content and str(payload.member) != "Björnbanan#6641":
        quote = message.content.split(" -")[0]
        if str(reaction) == "👉" or str(reaction) == "👌":
            change(quote, 1)
        if str(reaction) == "😠":
            change(quote, -1)


@bot.event
async def on_raw_reaction_remove(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    if str(message.author) == "Björnbanan#6641" and "_ _" in message.content and str(payload.member) != "Björnbanan#6641":
        quote = message.content.split(" -")[0]
        if str(reaction) == "👉" or str(reaction) == "👌":
            change(quote, -1)
        if str(reaction) == "😠":
            change(quote, 1)
    
    


@bot.command(pass_context=True, aliases=['j', '.join'])
async def join(ctx):
    log(ctx)
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True, aliases=['l', '.leave'])
async def leave(ctx):
    log(ctx)
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Not in a channel f u")


@bot.command(pass_context=True, aliases=['od', '.play_djungeltrubbaduren'])
async def play_djungel(ctx):
    log(ctx)
    song = os.path.isfile
    channel = ctx.message.author.voice.channel
    path = r"/home/pi/discordbot/songs/djungeltrubbaduren.mp3"
    await channel.connect()
    await ctx.send("God has entered the chat")
    vc = get(bot.voice_clients, guild=ctx.guild)
    vc.play(discord.FFmpegPCMAudio(path),
            after=lambda e: print("song is done"))
    vc.source = discord.PCMVolumeTransformer(vc.source)


@bot.command(pass_context=True, aliases=['erika', '.play_erika'])
async def play_cat(ctx):
    log(ctx)
    song = os.path.isfile
    channel = ctx.message.author.voice.channel
    path = r"/home/pi/discordbot/songs/erika.mp3"
    await channel.connect()
    await ctx.send("God has entered the chat")
    vc = get(bot.voice_clients, guild=ctx.guild)
    vc.play(discord.FFmpegPCMAudio(path),
            after=lambda e: print("song is done"))
    vc.source = discord.PCMVolumeTransformer(vc.source)


@bot.command(pass_context=True, aliases=['.create'])
async def create_team(ctx):
    log(ctx)
    author = ctx.message.author
    guild = ctx.guild
    roleid = get(guild.roles, id=774949686573793281)
    await author.add_roles(roleid)
    mentions = ctx.message.mentions
    mentions.append(author)
    role_name = author.display_name
    role = await guild.create_role(hoist=True, mentionable=True, name=role_name, colour=discord.Colour(0x0000FF))
    roleid = get(guild.roles, id=774952062760124487)
    for people in mentions:
        await people.remove_roles(roleid)
        await people.add_roles(role)


@bot.command(pass_context=True, aliases=['.skapa_kanaler'])
async def create_channels(ctx):
    log(ctx)
    author = ctx.message.author
    teamrole = author.roles[1]
    guild = ctx.guild
    name = teamrole.name
    category = await guild.create_category(name=name)
    everyone_role = guild.default_role
    await category.set_permissions(everyone_role, read_messages=False)
    overwrite = discord.PermissionOverwrite()
    overwrite.read_messages = True
    await category.set_permissions(teamrole, overwrite=overwrite)
    await guild.create_text_channel(name=name+"text", category=category)
    await guild.create_voice_channel(name=name+"voice", category=category)


@bot.command(pass_context=True, aliases=['obi', '.quote'])
async def quote_text(ctx):
    log(ctx)
    quote_list = json.load(open('/home/pi/discordbot/quote.json'))
    quote_nr = random.randint(0, len(quote_list)-1)
    message = quote_list[quote_nr]["quote"] + \
        " - "+quote_list[quote_nr]["author"] +"_ _"
    sent = await ctx.send(message)
    # 👉, 👌, 😠
    emojis = ['\U0001f449','\U0001f44C', '\U0001F620']
    for emoji in emojis:
        await sent.add_reaction(emoji)

@bot.command(pass_context=True, aliases=['obiv', '.quote_voice'])
async def quote_voice(ctx):
    log(ctx)
    quote_list = json.load(open('/home/pi/discordbot/quote.json'))
    quote_nr = random.randint(0, len(quote_list)-1)
    message = quote_list[quote_nr]["quote"] + \
        " - "+quote_list[quote_nr]["author"] +"_ _"
    sent = await ctx.send(message)
    # 👉, 👌, 😠
    emojis = ['\U0001f449','\U0001f44C', '\U0001F620']
    for emoji in emojis:
        await sent.add_reaction(emoji)

@bot.command(pass_context=True, aliases=['add', '.quote_add'])
async def quote_add(ctx):
    log(ctx)
    quote = ctx.message.content.split(' ', 1)
    quote = '"' + quote[1] + '"'
    author = ctx.message.author.name
    quote_list = json.load(open('/home/pi/discordbot/quote.json'))
    for quote_storage in quote_list:
        if quote_storage["quote"] == quote:
            await ctx.send("U sleezy copyrighter")
            return
    new_quote = {"quote": quote, "author": author, "rating": 1}
    quote_list.append(new_quote)
    with open('/home/pi/discordbot/quote.json', 'w') as file:
        json.dump(quote_list, file, indent=4)
    with open('/home/pi/discordbot/all_quote.json', 'w') as file:
        json.dump(quote_list, file, indent=4)
    message = "Added " + quote + " to the quote mind from " + author
    print("message= ", message)
    await ctx.send(message)


bot.remove_command('help')


@bot.command(pass_context=True, aliases=['help', '.help'])
async def help_commands(ctx):
    log(ctx)
    await ctx.send("**Commands**:\n Avaible at  https://fabbe90.gq/bjornbanan and yes I love milk.")


def log(ctx):
    print(ctx.message.created_at, " | ", ctx.message.guild.name, " | ",
          ctx.message.channel, " | ", ctx.message.author, " |\n", ctx.message.content)


bot.run(code)
