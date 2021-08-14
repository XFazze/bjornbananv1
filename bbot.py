import discord
from discord.ext import commands
import subprocess
import re

# Set prefix here
prefix = ","


# Add commands to load here
admin = ['channels.deletingchannel', 'channels.joinleavemessage', 'channels.rolelog', 'joinroles', 'reaction_roles', 'setprefix', 'channels.bettervc', 'delete_pinned']

games = []

info = ['avatar', 'guild', 'help', 'user', 'ping']

stats = ['actionlog', 'edited_messages', 'deleted_messages', 'joinleavelog', 'messagelog', 'tcstats', 'vcstats']

moderation = ['ban', 'banlist', 'kick', 'tempban', 'ticket', 'unban']

utilities = ['clear', 'colorcode', 'dnd', 'todo']

voice = ['basic_vc']


# Removes default help command and creates the bot object
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.remove_command('help')


# Loads all commands
allcogs = {"admin":admin, "games":games, "stats":games, "info":info, "moderation":moderation, "utilities":utilities, "voice":voice}
if __name__ == '__main__':
    for coglist in allcogs.keys():
        for cog in allcogs[coglist]:
            n = "cogs." + f"{str(coglist)}." + str(cog)
            bot.load_extension(n)


# Gets the token
token1, error = subprocess.Popen(["cat", "/tmp/discordbot/secrets.txt"], stdout=subprocess.PIPE).communicate()
token1 = re.split("'", str(token1))
token = token1[1].split(" ")

# Creates the bot event
@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help"))


bot.run(token[0])
