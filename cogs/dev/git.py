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
            embed = discord.Embed(title="Specify an action.", color=0xFD3333)
            await ctx.send(embed=embed)
        elif action == "pull":
            s = g.pull()
            embed = discord.Embed(color=0x00FF42)
            embed.add_field(name="Git pull", value=s)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Action does not exists.", color=0xFD3333)
            await ctx.send(embed=embed)
            
            
def setup(bot):
    bot.add_cog(Git(bot))