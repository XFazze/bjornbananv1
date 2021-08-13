# https://discord.com/api/oauth2/authorize?client_id=798491487917965323&permissions=8&scope=bot
import json
import discord
from discord.ext import commands
from cogwatch import Watcher

with open('/tmp/discordbot/secrets.txt', 'r') as f:
    secrets = f.read()
    secrets = secrets.split("\n")


async def determine_prefix(bot, message):
    prefixes = json.load(open('/tmp/discordbot/management/prefixes.json', 'r'))
    guild = message.guild
    if guild:
        return prefixes.get(str(guild.id), bot_prefix)
    else:
        return bot_prefix

intents = discord.Intents.all()
bot_prefix = 'f'
bot = commands.Bot(command_prefix=determine_prefix, intents=intents)   
bot.remove_command('help')


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    watcher = Watcher(bot, path="reloading_cogs", preload=True)
    await watcher.start()
    await bot.change_presence(activity=discord.Game(name="you | fhelp"))

bot.run(secrets[1])
