import discord
import json
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx):
        usr = ctx.message.mentions[0]
        await usr.ban(reason=None)
        '''
        try:
            usr = ctx.message.mentions[0]
            await self.ban(usr, reason="hej", deleted_message_days = 1)
            print("worked")
        except:
            await ctx.channel.send("You forgot to ping someone!!!!!!")
            print("fuck you")'''
    
    

def setup(bot):
    bot.add_cog(Base(bot))