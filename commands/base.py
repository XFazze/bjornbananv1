import discord
from discord.ext import commands


class Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def command(self, ctx):
        print("Template")
    

def setup(bot):
    bot.add_cog(Command(bot))