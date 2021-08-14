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
bot_prefix = 'g'
bot = commands.Bot(command_prefix=determine_prefix, intents=intents)
bot.remove_command('help')


admincogs = ['cogs.admin.channels.deletingchannel', 'cogs.admin.channel.joinleavemessage', 'cogs.admin.channels.rolelog', 'cogs.admin.enabledisable',
             'cogs.admin.joinroles', 'cogs.admin.reaction_roles', 'cogs.random.setprefix', 'cogs.admin.channels.bettervc']
gamescogs = []
infocogs = ['cogs.info.avatar', 'cogs.info.guild',
            'cogs.info.help', 'cogs.info.user']
loggingcogs = ['cogs.logging.actionlog', 'cogs.logging.edited_messages', 'cogs.logging.deleted_messages',
               'cogs.logging.edited_messages', 'cogs.logging.joinleavelog', 'cogs.logging.messagelog', 'cogs.logging.tcstats', 'cogs.logging.vcstats']
moderationcogs = ['cogs.moderation.ban', 'cogs.moderation.banlist', 'cogs.moderation.kick',
                  'cogs.moderation.tempban', 'cogs.moderation.ticket', 'cogs.moderation.unban']
randomcogs = ['cogs.random.clear', 'cogs.random.colorcode',
              'cogs.random.dnd', 'cogs.random.todo']
voicecogs = ['cogs.voice.basic_vc', ]
allcogs = [admincogs, gamescogs, infocogs, loggingcogs, infocogs,moderationcogs,randomcogs, voicecogs]

if __name__ == '__main__':
    for coglist in allcogs:
        for cog in coglist:
            bot.load_extension(cog)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    await bot.change_presence(activity=discord.Game(name="you | ghelp"))

bot.run(secrets[0])
