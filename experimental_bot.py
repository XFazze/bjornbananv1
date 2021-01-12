import discord
from discord.ext import commands
from codemy import code_ex

intents = discord.Intents.default()
intents.members = True
bot_prefix = 'f'
bot = commands.Bot(command_prefix=bot_prefix, Intents=intents)
bot.remove_command('help')


extensions = ['cogs.basic_vc', 'cogs.tournament', 'cogs.quote','cogs.simple', 'cogs.reaction_roles', 'cogs.dnd']
if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "n")
    await bot.change_presence(activity=discord.Game(name="you | fhelp"))

bot.run(code_ex)