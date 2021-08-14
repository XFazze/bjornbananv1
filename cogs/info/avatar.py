import discord
from discord.ext import commands
import random


class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.command(pass_context=True, aliases=['av'])
    async def avatar(self, ctx, member:discord.Member = None):
        if member is None:
            
            embed=discord.Embed(title=ctx.author, color=random.randint(0, 0xFFFFFF))
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        
        
        else:
            
            embed=discord.Embed(title=member, color=random.randint(0, 0xFFFFFF))
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(Avatar(bot))