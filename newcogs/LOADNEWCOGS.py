import discord
from discord.ext import commands
import os


class Cog_manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def loadnewcogs(self, ctx):
        self.bot.load_extension("newcogs.cog_manager")
        await ctx.send("loaded newcogs.cog_manager")


    @commands.command(pass_context=True)
    async def sex(self, ctx):
        for extension in self.bot.extensions:
            await ctx.send(extension)


    @commands.command(pass_context=True)
    async def unloadlastold(self, ctx):
        self.bot.unload_extension('cogs.dev.git')
        self.bot.unload_extension('cogs.dev.cog_manager')

    @commands.command(pass_context=True)
    async def unloadold(self, ctx):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        
        if len(os.listdir('./cogs')) > 1:
            for f in os.listdir('./cogs'):
                if f.endswith('.py'):
                    continue

                title = str(f)
                for f in os.listdir('./cogs/'+title):
                    if f.endswith('.py'):
                        cog = f"cogs.{title}.{str(f)[:-3]}"
                        if str(f) == 'uptime.py' or str(f) == 'cog_manager.py' or str(f) == 'git.py' :
                            continue
                       
                        try:
                            self.bot.unload_extension(cog)
                        except:
                            embed = discord.Embed(
                                title="Broken cog: " + cog, color=0xFD3333)
                            await ctx.send(embed=embed)


        embed = discord.Embed(title="Reloaded "+" all cogs", color=0x00FF42)
        await ctx.send(embed=embed)


   

def setup(bot):
    bot.add_cog(Cog_manager(bot))
