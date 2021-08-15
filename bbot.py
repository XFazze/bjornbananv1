import discord
import json
from discord.ext import commands
import subprocess
import re



# Add commands to load here
admin = ['joinroles',
         'reaction_roles',
         'bjornbanansetprefix',
         'channels.bettervc',
         'delete_pinned',
         'presence']

channels = ['joinleavemessage',
            'rolelog']

games = []

info = ['avatar',
        'guild',
        'help',
        'user',
        'ping',
        'cog',
        'uptime']

stats = ['tcstats',
         'vcstats']

logging = ['actionlog',
           'joinleavelog', 
           'messagelog',]

moderation = ['ban',
              'banlist',
              'kick',
              'tempban',
              'ticket',
              'unban',
              'edited_messages',
              'deleted_messages']

utilities = ['clear', 
             'colorcode', 
             'dnd', 
             'todo']

voice = ['basic_vc']

dev = ['errorhandler']

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
bot = commands.Bot(command_prefix=determine_prefix, intents=discord.Intents.all())
bot.remove_command('help')


# Loads all commands
allcogs = {"admin":admin, 
           "admin.channels":channels, 
           "games":games, 
           "stats":stats, 
           "stats.logging":logging, 
           "info":info, 
           "moderation":moderation, 
           "utilities":utilities, 
           "voice":voice,
           "dev":dev}

if __name__ == '__main__':
    for coglist in allcogs.keys():
        print(f"\n\n{coglist.capitalize()}")
        for cog in allcogs[coglist]:
            try:
                n = "cogs." + f"{str(coglist)}." + str(cog)
                print(f"LOADED      ::      {cog}")
                bot.load_extension(n)
            except commands.ExtensionFailed:
                print(f"UNLOADED      ::      {cog}")


# Gets the token
token1, error = subprocess.Popen(["cat", "/tmp/discordbot/secrets.txt"], stdout=subprocess.PIPE).communicate()
token1 = re.split("'", str(token1))
token = token1[1].split(" ")


# Creates the bot event
@bot.event
async def on_ready():
    print(f"\n\nLogged in as: {bot.user.name}\n")
    prefix  = determine_prefix
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help"))


bot.run(token[0])
