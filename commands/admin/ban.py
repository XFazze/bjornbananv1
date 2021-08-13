import discord
import json
from discord.ext import commands
import asyncio


# Command
class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member = None, *reason):
        
        # Sets default reason if not specified
        if not reason:
            reason = "Reason was not specified"
        
        # Bans member if the author has a higher role than the subject.
        if member is None:
            await ctx.send("Please mention someone to ban")
        
        else:
            
            if ctx.author.top_role.position > member.top_role.position:
                
                #r = []
                
                #for i in reason:
                    
                
                await ctx.send(f'{member} was banned with reason "{type(reason)}"')
                #await ctx.guild.ban(member, reason=str(reason))
                
            else:
                await ctx.send("The person you are trying to ban is more powerful than you")
            
        
    
    # Checks for errors
    @ban.error
    async def tempban_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to ban members.")
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Nucleus doesn't have permission to ban members.")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("The speccified member was not found")
    
    

def setup(bot):
    bot.add_cog(Ban(bot))