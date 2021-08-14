import discord
from discord.ext import commands
import subprocess
import re

# Set prefix here
prefix = ","


bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.remove_command('help')


admin = ['channels.deletingchannel', 'channels.joinleavemessage', 'channels.rolelog', 'enabledisable', 'joinroles', 'reaction_roles', 'setprefix', 'channels.bettervc', 'delete_pinned']

games = []

info = ['avatar', 'guild', 'help', 'user']

stats = ['actionlog', 'edited_messages', 'deleted_messages', 'joinleavelog', 'messagelog', 'tcstats', 'vcstats']

moderation = ['ban', 'banlist', 'kick', 'tempban', 'ticket', 'unban']

utilities = ['clear', 'colorcode', 'dnd', 'todo']

voice = ['basic_vc']






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


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help"))


bot.run(token[0])
