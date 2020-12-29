import discord, time, os, datetime, audioread, random, json
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
bot_prefix = 'g'
bot = commands.Bot(command_prefix=bot_prefix, Intents=intents)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "n ")
    await bot.change_presence(activity=discord.Activity(name="poppin fat kids in my school"))


@bot.command(pass_context=True, aliases=['j'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(datetime.datetime.now(), f"The bot has connected to {channel}\n")
    
    await ctx.send(f"Joined {channel}")

@bot.command(pass_context=True, aliases=['l'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(datetime.datetime.now(), f"The bot has left the channel")
        await ctx.send(f"Left {channel}")
    else:
        print(datetime.datetime.now(), "Bot was told to leave vc but not in vc")
        await ctx.send("Not in a channel f u")

@bot.command(pass_context=True, aliases=['od'])
async def play_djungel(ctx):
    print(datetime.datetime.now(), "playing")
    song  = os.path.isfile
    channel = ctx.message.author.voice.channel
    path = r"/home/pi/discordbot/djungeltrubbaduren.mp3"
    await channel.connect()
    await ctx.send("God has entered the chat")
    vc = get(bot.voice_clients, guild=ctx.guild)
    vc.play(discord.FFmpegPCMAudio(path), after=lambda e: print("song is done"))
    vc.source = discord.PCMVolumeTransformer(vc.source)

@bot.command(pass_context=True, aliases=['ud'])
async def play_cat(ctx):
    print(datetime.datetime.now(), "playing")
    song  = os.path.isfile
    channel = ctx.message.author.voice.channel
    path = r"/home/pi/discordbot/100_ways_to_love_a_cat.mp3"
    await channel.connect()
    await ctx.send("God has entered the chat")
    vc = get(bot.voice_clients, guild=ctx.guild)
    vc.play(discord.FFmpegPCMAudio(path), after=lambda e: print("song is done"))
    vc.source = discord.PCMVolumeTransformer(vc.source)

@bot.command(pass_context=True, aliases=['.create'])
async def create_team(ctx):
    author = ctx.message.author
    guild = ctx.guild
    roleid = get(guild.roles, id=774949686573793281)
    await author.add_roles(roleid)
    mentions = ctx.message.mentions
    mentions.append(author)
    role_name = author.display_name
    role = await guild.create_role(hoist=True, mentionable=True, name=role_name, colour=discord.Colour(0x0000FF))
    print("created team: ", role_name)
    roleid = get(guild.roles, id=774952062760124487)
    for people in mentions:
        await people.remove_roles(roleid)
        await people.add_roles(role)
        print("gave roll to", people.display_name)
    print("done creating")

@bot.command(pass_context=True, aliases=['.skapa_kanaler'])
async def create_channels(ctx):
    author = ctx.message.author
    teamrole = author.roles[1]
    print(teamrole)
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
    quote_list = json.load(open('/home/pi/discordbot/quote.json'))
    await ctx.send(quote_list[random.randint(0, len(quote_list)-1)])


bot.run('NzU5NTQxNDI1MDc4NTM0MTU0.X2_AEw.ybr5UaEUwTWmS40tRKzqS_MVW2k')