import discord
from discord.ext import commands
import random


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def user(self, ctx, member:discord.Member = None):
        
        if member is None:
            
            await ctx.send("Don't forget to mention someone")
        
        
        else:
            
            roles_list = ' | '.join(map(str, member.roles))
            
            embed=discord.Embed(title=member, color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="ID", value=member.id, inline=False)
            embed.add_field(name="Nickname", value=member.nick, inline=False)
            embed.add_field(name="Highest role", value=member.top_role, inline=False)
            embed.add_field(name="Roles", value=roles_list, inline=False)
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(User(bot))