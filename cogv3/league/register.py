from click import pass_context
import discord
from discord.ext import commands

from ..admin.managecommands import perms

# meddelande från fabian 
# spara riot puuid, alltså inte användarnamnet

class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.check(perms)
    async def register(self, ctx):
        pass
        