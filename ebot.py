import json
import discord
from discord.ext import commands
from codemy import code_ex


async def determine_prefix(bot, message):
    prefixes = json.load(open('management/prefixes.json', 'r'))
    guild = message.guild
    if guild:
        return prefixes.get(str(guild.id), bot_prefix)
    else:
        return bot_prefix

intents = discord.Intents.all()
bot_prefix = 'f'
bot = commands.Bot(command_prefix=determine_prefix, intents=intents)   
bot.remove_command('help')


extensions = ['cogs.voice.bettervc']



if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    await bot.change_presence(activity=discord.Game(name="you | fhelp"))

bot.run(code_ex)
