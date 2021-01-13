import json
import discord
from discord.ext import commands
from codemy import code


intents = discord.Intents.default()
intents.members = True
bot_prefix = 'g'


async def determine_prefix(bot, message):
    prefixes = json.load(open('prefixes.json', 'r'))
    guild = message.guild
    if guild:
        return prefixes.get(str(guild.id), bot_prefix)
    else:
        return bot_prefix

bot = commands.Bot(command_prefix=determine_prefix, Intents=intents)
bot.remove_command('help')


extensions = ['cogs.basic_vc', 'cogs.tournament', 'cogs.quote',
              'cogs.simple', 'cogs.reaction_roles', 'cogs.dnd']
if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    await bot.change_presence(activity=discord.Game(name="you | ghelp"))

bot.run(code)
