import discord
from discord.ext import commands
import asyncio


# Command
class Tempban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def tempban(self, ctx, member:discord.Member = None, days = None, *reason):
        # Sets default time and reason if not specified
        if days is None:
            days = 7
            
        if reason is None:
            reason = "Reason was not specified"
        
        
        # Bans member for the specified time if a member is mentioned and if the author has a higher role than the subject.
        if member is None:
            await ctx.send("Please mention someone to ban")
        
        
        else:
            
            if ctx.author.top_role.position > member.top_role.position:
                
                reason = ' '.join(map(str, reason))
                
                t = int(days)*24*60*60
                
                await ctx.send(f'{member} was banned with reason "{reason}" for {int(t/60/60/24)} days')
                    
                await ctx.guild.ban(member, reason=reason)
                
                await asyncio.sleep(t)
                await member.unban()
                
            
            else:
                await ctx.send("The person you are trying to ban is more powerful than you")
            
        
    
    # Checks for errors
    @tempban.error
    async def tempban_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to ban members.")
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Nucleus doesn't have permission to ban members.")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("The speccified member was not found")
    
    

def setup(bot):
    bot.add_cog(Tempban(bot))