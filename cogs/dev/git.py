from click import pass_context
import discord
from discord.ext import commands
import git

g = git.cmd.Git("")

class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def git(self, ctx, action = None):
        if not str(ctx.author) == "mega#2222" and  not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("You're noone")
            return
        
            
        if action == None:
            await ctx.send("Specify an action")
        else:
            await ctx.send("Success")
    
def setup(bot):
    bot.add_cog(Git(bot))