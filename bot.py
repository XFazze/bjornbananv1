import discord
import time
import os
import datetime
import audioread
import random
import json
import ffmpeg
import re
from  gtts import gTTS
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


@bot.command(pass_context=True, aliases=['j', '.join'])
async def join(ctx):
    log(ctx)
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
        print(f"moved to a channel{channel}")
    else:
        voice = await channel.connect()
        print(f"connected to a channel{channel}")

    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True, aliases=['l', '.leave'])
async def leave(ctx):
    log(ctx)
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
        print(f"Left channel:{channel}")
    else:
        await ctx.send("Not in a channel f u")
        print(f"was asked to leave but not in channel{channel}")


@bot.command(pass_context=True, aliases=['od', '.play_djungeltrubbaduren'])
async def play_djungel(ctx):
    log(ctx)
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    path = r"/home/pi/discordbot/songs/djungeltrubbaduren.mp3"
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send("God has entered the chat")
    vc = get(bot.voice_clients, guild=ctx.guild)
    vc.play(discord.FFmpegPCMAudio(path),
            after=lambda e: print("song is done"))
    vc.source = discord.PCMVolumeTransformer(vc.source)


@bot.command(pass_context=True, aliases=['erika', '.play_erika'])
async def play_cat(ctx):
    log(ctx)
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
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
    quote_list = json.load(open('/home/pi/discordbot/quote/quote.json'))
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
    quote_list = json.load(open('/home/pi/discordbot/quote/quote.json'))
    quote_nr = random.randint(0, len(quote_list)-1)
    message = "at your service"+"_ _"
    sent = await ctx.send(message)
    quote = quote_list[quote_nr]["quote"].replace('"', '')
  
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    path = r"/home/pi/discordbot/quote/voice/"+quote+".mp3"
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send("God has entered the chat")
    vc = get(bot.voice_clients, guild=ctx.guild)
    vc.play(discord.FFmpegPCMAudio(path),
            after=lambda e: print("song is done"))
    vc.source = discord.PCMVolumeTransformer(vc.source)
    emojis = ['\U0001f449','\U0001f44C', '\U0001F620']
    for emoji in emojis:
        await sent.add_reaction(emoji)

@bot.command(pass_context=True, aliases=['add', '.quote_add'])
async def quote_add(ctx):
    log(ctx)
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



@bot.event
async def on_raw_reaction_add(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    if str(message.author) == "Björnbanan#6641" and "_ _" in message.content and str(payload.member) != "Björnbanan#6641":
        quote = message.content.split(" -")[0]
        quote = quote[:-3]
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
        quote = quote[:-3]
        if str(reaction) == "👉" or str(reaction) == "👌":
            change(quote, -1)
        if str(reaction) == "😠":
            change(quote, 1)

bot.remove_command('help')


@bot.command(pass_context=True, aliases=['help', '.help'])
async def help_commands(ctx):
    log(ctx)
    await ctx.send("**Commands**:\n Avaible at  https://fabbe90.gq/bjornbanan and yes I love milk.")


@bot.command(pass_context=True, aliases=['color', '.color'])
async def farg(ctx):
    log(ctx)
    for role in ctx.message.author.roles:
        if str(role)[0] == ";":
            if len(str(ctx.message.content).split(" "))>1:
                if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', "#"+str(ctx.message.content).split(" ")[1]):
                    await role.edit(color=int(("0x"+str(ctx.message.content).split(" ")[1]),16), reason="Testing")
                    print("successfully changed color")
                    await ctx.send("Successfully changed Color of your role")
                    return
                else:
                    await ctx.send("Colorcode is invalid format:gcolor ffffff")
                    print("Invalid colorcode")
                    return
            else:
                print("no code provided")
                await ctx.send("You need to provide a color code like this:gcolor ffffff")
                return
    await ctx.send("You dont have a role")

@bot.command(pass_context=True, aliases=['rr', '.reactionroles'])
@commands.has_permissions(manage_roles=True)
async def reaction_role(ctx):
    log(ctx)
    try:
        role_id=int(str(ctx.message.content).split(" ")[1][3:-1])
    except:
        print("forgot variable role")
        await ctx.send("you forgot the role variable, format: grr @role emoji text. OBS spaces")
        return
    try:
        emoji=str(ctx.message.content).split(" ")[2]
    except:
        print("forgot variable emoji")
        await ctx.send("you forgot the amoji variable, format: grr @role emoji text. OBS spaces")
        return
    try:
        text=str(ctx.message.content).split(" ")[3:]
    except:
        print("forgot variable text")
        await ctx.send("you forgot the text variable, format: grr @role emoji text. OBS spaces")
        return
    highest_role=ctx.message.author.roles[-1]
    role = get(ctx.guild.roles, id=role_id)
    for roles in ctx.guild.roles:
        if role == roles:
            print("He's allowed")
            break
        elif highest_role == roles:
            print("he's not allowed")
            return 
    phrase=""
    for word in text:
        phrase = phrase+" "+word
    message = "Role: "+str(role) +" |"+ phrase

    bot_message = await ctx.send(message)
    await bot_message.add_reaction(emoji)
    await ctx.message.delete()


# send command role, text and reaction
# create message with > text
# react to message
# add on react check if ">" is in message
# react.user adds role
@bot.event
async def on_raw_reaction_add(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    if str(message.author) == "Björnbanan#6641" and "Role:" == str(message.content)[0:5] and str(payload.member) != "Björnbanan#6641":
        print("yeeees")
        role = str(message.content)[6:].split(" |")[0]
        role = discord.utils.get(payload.member.roles,name=role)
        print(type(role))
        await payload.member.add_roles(role)

 


@bot.event
async def on_raw_reaction_remove(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    if str(message.author) == "Björnbanan#6641" and "Role:" == str(message.content)[0:5] and str(payload.member) != "Björnbanan#6641":
        print("REEEEEEEEE")


def log(ctx):
    print(ctx.message.created_at, " | ", ctx.message.guild.name, " | ",
          ctx.message.channel, " | ", ctx.message.author, " |\n", ctx.message.content)


bot.run(code)