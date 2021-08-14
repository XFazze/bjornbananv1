# https://discord.com/oauth2/authorize?client_id=775007176157954058&scope=bot&permissions=8589934591

import json
import discord
from discord.ext import commands
import asyncio
from cogwatch import Watcher
import getpass

with open(f'config/config.txt', 'r') as f:
    secrets = f.read()
    secrets = secrets.split("\n")


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='n.', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    watcher = Watcher(bot, path=f"commands", preload=True)
    await watcher.start()
    await bot.change_presence(activity=discord.Game(name="n.help"))


bot.run(secrets[0])
