import discord
from discord.ext import commands


# Command
class Banlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def banlist(self, ctx):
        
        await ctx.message.delete()
        
        banlist = await ctx.guild.bans()
        
        for i in range(0, len(banlist)):
            
            embed=discord.Embed(title="Banned member", color=0xff0000)
            embed.add_field(name="User", value=banlist[i].user, inline=False)
            embed.add_field(name="ID", value=banlist[i].user.id, inline=False)
            embed.add_field(name="Reason", value=banlist[i].reason, inline=False)
            await ctx.send(embed=embed)
            

def setup(bot):
    bot.add_cog(Banlist(bot))





