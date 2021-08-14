# https://discord.com/api/oauth2/authorize?client_id=798491487917965323&permissions=8&scope=bot
import json
import discord
from discord.ext import commands
from cogwatch import Watcher

with open('config/config.txt', 'r') as f:
    secrets = f.read()
    secrets = secrets.split("\n")


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="f.", intents=intents)   


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    watcher = Watcher(bot, path="reloading_cogs", preload=True)
    await watcher.start()
    await bot.change_presence(activity=discord.Game(name="you | fhelp"))

bot.run(secrets[0])
