import discord
from discord.ext import commands
import os


class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command(pass_context=True)
    async def load_cog(self, ctx, category = None, cog = None):
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        if category == None:
            embed = discord.Embed(title="Cogs", color=0xFFFFFF)
            if len(os.listdir('./cogs')) > 1:
                for f in os.listdir('./cogs'):
                    if f.endswith('.py'):
                        continue

                    title=str(f)
                    commands = ''
                    for f in os.listdir('./cogs/'+title):
                        if f.endswith('.py'):
                            commands += str(f)+'\n'
                    embed.add_field(name=title, value=commands)
        
            await ctx.send(embed=embed)




    @commands.command(pass_context=True)
    async def cog(self, ctx, category = None, cog = None):
        if category == None:
            await ctx.send(f"Usage: ,cog *(category)* *(command)*")
        elif category == "categories":
            await ctx.send(f"admin, admin.channels, games, info, moderation, stats, stats.logging, utilities, voice")
        elif cog == None:
            await ctx.send(f"Usage: ,cog *(category)* *(command)*")
        else:
            try:
                self.bot.load_extension(f"cogs.{category}.{cog}")
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"**{cog}** is already loaded")
            except commands.ExtensionNotFound:
                await ctx.send(f"There is no cog named {cog}")
            else:
                await ctx.send("Cog is unloaded")
                self.bot.unload_extension(f"cogs.{cog}")
        
    

def setup(bot):
    bot.add_cog(Cogs(bot))