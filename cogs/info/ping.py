import discord
import json
from discord.ext import commands
from discord.ext.commands import bot


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, aliases=['latency'])
    async def ping(self, ctx):
        print(dir(self))
        embed = discord.Embed(colour=0xFFFFFF)
        embed.add_field(name="Uptime", value='{0}ms'.format(round(self.bot.latency, 1)))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Base(bot))