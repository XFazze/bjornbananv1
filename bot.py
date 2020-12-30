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

intents = discord.Intents.default()
intents.members = True
bot_prefix = 'g'
bot = commands.Bot(command_prefix=bot_prefix, Intents=intents)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "n")
    await bot.change_presence(activity=discord.Game(name="you | ghelp"))


@bot.command(pass_context=True, aliases=['j'])
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


@bot.command(pass_context=True, aliases=['l'])
async def leave(ctx):
    log(ctx)
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Not in a channel f u")


@bot.command(pass_context=True, aliases=['od'])
async def play_djungel(ctx):
    log(ctx)
    song = os.path.isfile
    channel = ctx.message.author.voice.channel
    path = r"/home/pi/discordbot/djungeltrubbaduren.mp3"
    await channel.connect()
    await ctx.send("God has entered the chat")
    vc = get(bot.voice_clients, guild=ctx.guild)
    vc.play(discord.FFmpegPCMAudio(path),
            after=lambda e: print("song is done"))
    vc.source = discord.PCMVolumeTransformer(vc.source)


@bot.command(pass_context=True, aliases=['erika'])
async def play_cat(ctx):
    log(ctx)
    song = os.path.isfile
    channel = ctx.message.author.voice.channel
    path = r"/home/pi/discordbot/erika.mp3"
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


@bot.command(pass_context=True, aliases=['odi'])
async def quote_text(ctx):
    log(ctx)
    quote_list = json.load(open('/home/pi/discordbot/quote.json'))
    await ctx.send(quote_list[random.randint(0, len(quote_list)-1)])

bot.remove_command('help')


@bot.command(pass_context=True, aliases=['help'])
async def help_commands(ctx):
    log(ctx)
    await ctx.send("**Commands**:\n Avaible at  https://fabbe90.gq/bjornbanan and yes I love milk.")


    
def log(ctx):
    print(ctx.message.created_at, " | ", ctx.message.guild.name, " | ", ctx.message.channel, " | ", ctx.message.author, " |\n", ctx.message.content)

bot.run('NzU5NTQxNDI1MDc4NTM0MTU0.X2_AEw.ybr5UaEUwTWmS40tRKzqS_MVW2k')
