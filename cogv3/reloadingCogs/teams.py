import discord
from pymongo import MongoClient
from discord.ext import commands
from discord_slash  import cog_ext, SlashContext



class teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @cog_ext.cog_slash(name='recommendTeams', pass_context=True, aliases=['rt'])
    async def recommendTeams(self, ctx:SlashContext):
        await ctx.send('working')
        pass

def setup(bot):
    bot.add_cog(teams(bot))