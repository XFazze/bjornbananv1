import discord
import json
from discord.ext import commands
import random


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def user(self, ctx, object):
        if object == "avatar":
            embed=discord.Embed(title="Avatar", color=random.randint(0, 0xFFFFFF))
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        
        else:
            await ctx.send(f"Please specify: icon")

def setup(bot):
    bot.add_cog(User(bot))