import discord
import json
from discord.ext import commands
import subprocess
import re

# Set prefix here
bot_prefix = ","


async def determine_prefix(bot, message):
    prefixes = json.load(open('/tmp/discordbot/management/prefixes.json', 'r'))
    guild = message.guild
    if guild:
        return prefixes.get(str(guild.id), bot_prefix)
    else:
        return bot_prefix

# Removes default help command and creates the bot object
bot = commands.Bot(command_prefix=determine_prefix,
                   intents=discord.Intents.all())
bot.remove_command('help')

if __name__ == '__main__':
    bot.load_extension('cogs.dev.cog_manager')
    bot.load_extension('cogs.info.uptime')


# Gets the token
token1, error = subprocess.Popen(
    ["cat", "/tmp/discordbot/secrets.txt"], stdout=subprocess.PIPE).communicate()
token1 = re.split("'", str(token1))
token = token1[1].split(" ")


# Creates the bot event
@bot.event
async def on_ready():
    print(f"\n\nLogged in as: {bot.user.name}\n")
    prefix = determine_prefix
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help"))


bot.run(token[0])
