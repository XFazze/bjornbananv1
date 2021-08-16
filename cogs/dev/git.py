import discord
from discord.ext import commands
import git

g = git.cmd.Git("")

class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def git(self, ctx, action = None):
        if action == None:
            await ctx.send("Specify an action")
        elif action == "pull":
            print("bitchhhh")
            #result = g.pull()
            #print(result)
    
def setup(bot):
    bot.add_cog(Git(bot))