import discord
from discord.ext import commands

import os


# Commands

adminCommands = ""

moderationCommands = "ban \ntempban \nunban \nkick \n"

infoCommands = "guild \nuser \nbanlist \n"

voiceCommands = ""

loggingCommands = ""

randomCommands = ""




class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="Prefix: **n.**", color=0xFFFFFF)
        
        if len(os.listdir('./commands/admin')) > 0:
            for filename in os.listdir('./commands/admin'):
                if filename.endswith('.py'):
                    embed.add_field(name="Admin", value=filename[:-3])
        
        
        
        
        if len(os.listdir('./commands/info')) > 0:
            infoCommands = "h"
            for filename in os.listdir('./commands/info'):
                if filename.endswith('.py'):
                    infoCommands.join(f"{filename[:-3]}\n")
            embed.add_field(name="Info", value=infoCommands)
        
        
        
        
        if len(os.listdir('./commands/logging')) > 0:
            for filename in os.listdir('./commands/logging'):
                if filename.endswith('.py'):
                    embed.add_field(name="Logging", value=filename[:-3])
        
        if len(os.listdir('./commands/moderation')) > 0:
            for filename in os.listdir('./commands/moderation'):
                if filename.endswith('.py'):
                    embed.add_field(name="Moderation", value=filename[:-3])
        
        if len(os.listdir('./commands/random')) > 0:
            for filename in os.listdir('./commands/random'):
                if filename.endswith('.py'):
                    embed.add_field(name="Random", value=filename[:-3])
        
        if len(os.listdir('./commands/voice')) > 0:
            for filename in os.listdir('./commands/voice'):
                if filename.endswith('.py'):
                    embed.add_field(name="Voice", value=filename[:-3])
        
        '''if len(adminCommands) > 0:    
            embed.add_field(name="Admin", value=adminCommands, inline=False)
        
        if len(moderationCommands) > 0:
            embed.add_field(name="Moderation", value=moderationCommands, inline=False)
            
        if len(infoCommands) > 0:
            embed.add_field(name="Info", value=infoCommands, inline=False)
            
        if len(voiceCommands) > 0:
            embed.add_field(name="Voice", value=voiceCommands, inline=False)
            
        if len(loggingCommands) > 0:
            embed.add_field(name="Logging", value=loggingCommands, inline=False)
        
        if len(randomCommands) > 0:
            embed.add_field(name="Random", value=randomCommands, inline=False)'''
            
        
            
            
        await ctx.send(embed=embed)
    
    
    
def setup(bot):
    bot.add_cog(Help(bot))