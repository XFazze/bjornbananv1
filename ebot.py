# https://discord.com/api/oauth2/authorize?client_id=798491487917965323&permissions=8&scope=bot
import subprocess
import re
import discord
from discord.ext import commands
from cogwatch import Watcher


bot = commands.Bot(command_prefix="f.", intents=discord.Intents.all())   
bot.remove_command('help')


# Gets the token
token1, error = subprocess.Popen(["cat", "/tmp/discordbot/secrets.txt"], stdout=subprocess.PIPE).communicate()
token1 = re.split("'", str(token1))
token = token1[1].split(" ")


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    watcher = Watcher(bot, path="reloading_cogs", preload=True)
    await watcher.start()
    await bot.change_presence(activity=discord.Game(name="you | fhelp"))

#print(token)
bot.run(token[1])
