import discord
import json
from discord.ext import commands


class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def guild(self, ctx, *info):
        if info[0] == "icon":
            await ctx.send(ctx.guild.icon_url)
        elif info[0] == "owner":
            await ctx.send(ctx.guild.owner)
        else:
            await ctx.send(f"Please specify: icon, banner, owner")
    
    @guild.error
    async def guild_error(self, ctx, error):
        await ctx.send(f"Please specify: icon, banner, owner")

def setup(bot):
    bot.add_cog(Guild(bot))