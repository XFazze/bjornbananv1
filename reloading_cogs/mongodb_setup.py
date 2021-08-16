import discord
import json
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mdbguild(self, ctx):
        docs = []
        for guild in self.bot.guilds:
            text_channels = []
            for channel in guild.text_channels:
                text_channels.append()

            doc = {"name": guild.name,
                   "id": guild.id,
                   "": guild.id }
            print(guild)


def setup(bot):
    bot.add_cog(Base(bot))
