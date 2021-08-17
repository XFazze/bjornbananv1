import discord, datetime, time
from discord.ext import commands

start_time = time.time()



class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, name="uptime", aliases=[], description="", usage="uptime")
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xFFFFFF)
        embed.add_field(name="Uptime", value=text)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)
    

def setup(bot):
    bot.add_cog(Uptime(bot))