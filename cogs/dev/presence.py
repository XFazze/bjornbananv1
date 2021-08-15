import discord
from discord.ext import commands


class Presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def presence(self, ctx, presence = None):
        if str(ctx.author) == "mega#2222" or str(ctx.author) == "AbstractNucleus#6969":
            pass
        else:
            await ctx.send("Youre noone")
        if presence == None:
            await ctx.send("Specify a presence")
        else:
            await self.bot.change_presence(activity=discord.Game(name=presence))
            await ctx.send("Success")
        
    

def setup(bot):
    bot.add_cog(Presence(bot))