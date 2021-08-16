import discord
from discord.ext import commands
import subprocess


class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def git(self, ctx, action):
        if action == "pull":
            result, error = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE).communicate()
            print(result)
    
def setup(bot):
    bot.add_cog(Git(bot))