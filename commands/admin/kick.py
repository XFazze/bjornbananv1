import discord
import json
from discord.ext import commands


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member, reason = None):
        if reason is None:
            reason = "Reason was not specified"
        
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} was kicked with reason "{reason}"')
    
    
    @kick.error
    async def kick_error(self, ctx, error):
        await ctx.send("Please mention someone to kick")
    
    

def setup(bot):
    bot.add_cog(Kick(bot))