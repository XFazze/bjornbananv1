import discord
import json
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Base(bot))