import discord
from discord.ext import commands
import subprocess
import re

# Set prefix here
prefix = ","


# Add commands to load here
admin = ['joinroles',
         'reaction_roles',
         'setprefix',
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
           'messagelog',
           'edited_messages',
           'deleted_messages']

moderation = ['ban',
              'banlist',
              'kick',
              'tempban',
              'ticket',
              'unban']

utilities = ['clear', 
             'colorcode', 
             'dnd', 
             'todo', 
             'errorhandler']

voice = ['basic_vc']



# Removes default help command and creates the bot object
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
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
           "voice":voice}

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
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help"))


bot.run(token[0])
