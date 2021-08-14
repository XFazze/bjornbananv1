import json
import discord
from discord.ext import commands

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
bot_prefix = ','
bot = commands.Bot(command_prefix=determine_prefix, intents=intents)
bot.remove_command('help')


admincogs = ['cogs.admin.channels.deletingchannel', 'cogs.admin.channels.joinleavemessage', 'cogs.admin.channels.rolelog', 'cogs.admin.enabledisable',
             'cogs.admin.joinroles', 'cogs.admin.reaction_roles', 'cogs.admin.setprefix', 'cogs.admin.channels.bettervc', 'cogs.admin.delete_pinned']
gamescogs = []
infocogs = ['cogs.info.avatar', 'cogs.info.guild',
            'cogs.info.help', 'cogs.info.user']
loggingcogs = ['cogs.stats.logging.actionlog','cogs.stats.logging.joinleavelog', 'cogs.stats.logging.messagelog', 'cogs.stats.tcstats', 'cogs.stats.vcstats']
moderationcogs = ['cogs.moderation.ban', 'cogs.moderation.banlist', 'cogs.moderation.kick', 'cogs.moderation.tempban',
                  'cogs.moderation.ticket', 'cogs.moderation.deleted_messages', 'cogs.moderation.edited_messages', 'cogs.moderation.unban']
randomcogs = ['cogs.random.clear', 'cogs.random.colorcode',
              'cogs.random.dnd', 'cogs.random.todo', 'cogs.random.bomb_reactions']
voicecogs = ['cogs.voice.basic_vc', ]
allcogs = [admincogs, gamescogs, loggingcogs,
           infocogs, moderationcogs, randomcogs, voicecogs]

if __name__ == '__main__':
    for coglist in allcogs:
        for cog in coglist:
            bot.load_extension(cog)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    await bot.change_presence(activity=discord.Game(name=","))

bot.run(secrets[0])
