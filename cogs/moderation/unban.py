import discord
from discord.ext import commands


# Command
class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, member = None):

        # Unbans a member
        if member is None:
            await ctx.send("Please mention someone to unban")
        
        else:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")
            
            for ban_entry in banned_users:
                user = ban_entry.user
                
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'{user} was unbanned')

    

def setup(bot):
    bot.add_cog(Unban(bot))