import discord
from discord.ext import commands
import subprocess
import git



class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def git(self, ctx, action):
        if action == "pull":
            g = git.cmd.Git("")
            result = g.pull()
            print(result)
    
def setup(bot):
    bot.add_cog(Git(bot))