import json
import discord
from discord.ext import commands
from codemy import code_m


async def determine_prefix(bot, message):
    prefixes = json.load(open('/tmp/discordbot/management/musicprefixes.json', 'r'))
    guild = message.guild
    if guild:
        return prefixes.get(str(guild.id), bot_prefix)
    else:
        return bot_prefix

intents = discord.Intents.all()
bot_prefix = 'b'
bot = commands.Bot(command_prefix=determine_prefix, intents=intents)
bot.remove_command('help')


extensions = ['cogs.voice.musicbot']


if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    await bot.change_presence(activity=discord.Game(name="you | bhelp"))

bot.run('ODI0MDQxMDQxMzEyNDgxMzEx.YFpmBg.l52vEMTos9e_7XPbbUP20G6TSEs')
