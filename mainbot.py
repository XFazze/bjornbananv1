import json
import discord
from discord.ext import commands
from codemy import code


async def determine_prefix(bot, message):
    prefixes = json.load(open('management/prefixes.json', 'r'))
    guild = message.guild
    if guild:
        return prefixes.get(str(guild.id), bot_prefix)
    else:
        return bot_prefix

intents = discord.Intents.all()
bot_prefix = 'g'
bot = commands.Bot(command_prefix=determine_prefix, intents=intents)
bot.remove_command('help')


extensions = ['cogs.admin.deletingchannel', 'cogs.admin.enabledisable', 'cogs.admin.joinroles', 'cogs.admin.reaction_roles', 'cogs.admin.ticket',
              'cogs.logging.actionlog', 'cogs.logging.rolelog', 'cogs.logging.tcstats', 'cogs.logging.vcstats', 'cogs.random.dnd', 'cogs.random.maslog',
              'cogs.random.shroud', 'cogs.random.simple', 'cogs.voice.basic_vc', 'cogs.voice.bettervc']


if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    await bot.change_presence(activity=discord.Game(name="you | ghelp"))

bot.run(code)
