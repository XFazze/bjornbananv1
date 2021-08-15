import discord
from discord.ext import commands
import random


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, aliases=['serverinfo'])
    async def server(self, ctx):
        
        await ctx.message.delete()
        
        
        embed=discord.Embed(title=ctx.guild, color=random.randint(0, 0xFFFFFF))
        embed.add_field(name="Owner", value=ctx.guild.owner, inline=False)
        embed.add_field(name="ID", value=ctx.guild.id, inline=False)
        embed.add_field(name="Member count", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Creation Date", value=ctx.guild.created_at, inline=False)
        embed.add_field(name="Region", value=ctx.guild.region, inline=False)
        embed.add_field(name="Number of text channels", value=len(ctx.guild.text_channels), inline=False)
        embed.add_field(name="Number of voice channels", value=len(ctx.guild.voice_channels), inline=False)
        embed.add_field(name="Number of categories", value=len(ctx.guild.categories), inline=False)
        
        
        embed.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
        
        
        
        

def setup(bot):
    bot.add_cog(Server(bot))