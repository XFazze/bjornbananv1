# https://discord.com/oauth2/authorize?client_id=775007176157954058&scope=bot&permissions=8589934591

import discord
from discord.ext import commands
from cogwatch import Watcher
import subprocess
import re


# Set prefix here
prefix = "n."


# Removes default help command and creates the bot object
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')


# When the bot starts
@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    watcher = Watcher(bot, path=f"commands", preload=True)
    await watcher.start()
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help"))


# Gets the token
token, error = subprocess.Popen(["cat", "config.txt"], stdout=subprocess.PIPE).communicate()
token = re.split("b|'", str(token))


# Starts the bot
bot.run(token[2])