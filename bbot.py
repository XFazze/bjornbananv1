import discord
import json
from discord.ext import commands
from pymongo import MongoClient

# Set prefix here
prefix = ","

# FIXME editing prefix doesnt work

async def determine_prefix(bot, message):
    prefixes = json.load(open('/tmp/discordbot/management/prefixes.json', 'r'))
    guild = message.guild
    if guild:
        return prefixes.get(str(guild.id), prefix)
    else:
        return prefix

# Removes default help command and creates the bot object
bot = commands.Bot(command_prefix=',', intents=discord.Intents.all())
# bot.remove_command('help')


# Gets the token
collection = MongoClient('localhost', 27017).maindb.tokens
myquery = {"botName": 'bbot'}
doc = collection.find_one(myquery)
if not doc:
    raise ValueError('Token not found in mongodb database.')
token = doc['token']

# Creates the bot event


@bot.event
async def on_ready():
    print(f"\n\nLogged in as: {bot.user.name}\n")
    await bot.change_presence(activity=discord.Game(name=f",help | fabbe90.gq"))


if __name__ == '__main__':
    bot.load_extension('cogv3.dev.cog_manager')
    bot.run(token)
