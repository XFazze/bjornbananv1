import discord
import random
from discord.ext import commands


class Base(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, aliases=['rol', '.roll'])
    async def roll(self,ctx):
        try:
            rollamount = int(ctx.message.content.split(" ")[1])
        except:
            print("didnt provide number")
            await ctx.send("You didnt provide a number")
            return
        outcome = random.randint(1,rollamount)
        await ctx.send(f"You got a {outcome}")
        print("done")
        

def setup(bot):
    bot.add_cog(Base(bot))