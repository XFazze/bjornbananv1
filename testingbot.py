# https://discord.com/oauth2/authorize?client_id=775007176157954058&scope=bot&permissions=8589934591

from pydoc import cli
import discord
import json
from discord.ext import commands
import subprocess
import re
import pymongo
from cogwatch import Watcher



# Set prefix here
prefix = "n."





async def determine_prefix(bot, message):
    prefixes = json.load(open('/tmp/discordbot/management/prefixes.json', 'r'))
    guild = message.guild
    if guild:
        return prefixes.get(str(guild.id), prefix)
    else:
        return prefix


# Removes default help command and creates the bot object
bot = commands.Bot(command_prefix=determine_prefix, intents=discord.Intents.all())
bot.remove_command('help')




# When the bot starts
@bot.event
async def on_ready():
    print(f"\n\nLogged in as: {bot.user.name}\n")
    prefix = determine_prefix
    watcher = Watcher(bot, path="testingcogs", preload=True)
    await watcher.start()
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help"))


# Gets the token
token, error = subprocess.Popen(["cat", "config.txt"], stdout=subprocess.PIPE).communicate()
token = re.split("b|'", str(token))


# Starts the bot
bot.run(token[2])