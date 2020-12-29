import discord
import audioread
import time

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')



@client.event
async def on_voice_state_update(member: discord.Member, before, after):
#replace this with the path to your audio file
    path = r"/home/xfazze/mein-fuhrer/discordbot/djungeltrubbaduren.mp3"

    vc_before = before.channel
    vc_after = after.channel
    if vc_before == vc_after:
        return
    if vc_before is None:
        channel = member.voice.channel
        vc = await channel.connect()
        time.sleep(.5)
        vc.play(discord.FFmpegPCMAudio(path))
        with audioread.audio_open(path) as f:
            #Start Playing
            time.sleep(f.duration)
        await vc.disconnect()

    elif vc_after is None:
        return
    else:
        channel = member.voice.channel
        time.sleep(.5)
        vc.play(discord.FFmpegPCMAudio(path))
        with audioread.audio_open(path) as f:
            #Start Playing
            time.sleep(f.duration)
        await vc.disconnect()

