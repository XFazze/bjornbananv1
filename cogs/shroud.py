import discord
from discord.ext import commands
from discord.utils import get


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, aliases=['newmembers'])
    async def newmemberss(self, ctx):
        guild = ctx.guild
        for member in guild.members:
            if len(member.roles) == 1:
                message = "user: "+member.name
                await ctx.send(message)
    
    @commands.command(pass_context=True, aliases=['prime'])
    @commands.has_permissions(manage_roles=True)
    async def prive(self, ctx):
        guild = ctx.guild
        for member in ctx.message.mentions:
            role = get(guild.roles, id=802300233103048704)
            await member.add_roles(role)
            
            role = get(guild.roles, id=802305915491319838)
            await member.remove_roles(role)
        

def setup(bot):
    bot.add_cog(Base(bot))