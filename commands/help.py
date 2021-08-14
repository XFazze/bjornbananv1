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
            adminCommands = ""
            for f in os.listdir('./commands/admin'):
                if f.endswith('.py'):
                    adminCommands += f"{f[:-3]}\n"
            embed.add_field(name="Admin", value=adminCommands, inline=False)
        
        if len(os.listdir('./commands/moderation')) > 0:
            moderationCommands = ""
            for f in os.listdir('./commands/moderation'):
                if f.endswith('.py'):
                    moderationCommands += f"{f[:-3]}\n"
            embed.add_field(name="Moderation", value=moderationCommands, inline=False)
        
        if len(os.listdir('./commands/info')) > 0:
            infoCommands = ""
            for f in os.listdir('./commands/info'):
                if f.endswith('.py'):
                    infoCommands += f"{f[:-3]}\n"
            embed.add_field(name="Info", value=infoCommands, inline=False)
            
        if len(os.listdir('./commands/voice')) > 0:
            voiceCommands = ""
            for f in os.listdir('./commands/voice'):
                if f.endswith('.py'):
                    voiceCommands += f"{f[:-3]}\n"
            embed.add_field(name="Voice", value=voiceCommands, inline=False)
            
        if len(os.listdir('./commands/logging')) > 0:
            loggingCommands = ""
            for f in os.listdir('./commands/logging'):
                if f.endswith('.py'):
                    loggingCommands += f"{f[:-3]}\n"
            embed.add_field(name="Logging", value=loggingCommands, inline=False)
            
        if len(os.listdir('./commands/random')) > 0:
            randomCommands = ""
            for f in os.listdir('./commands/random'):
                if f.endswith('.py'):
                    randomCommands += f"{f[:-3]}\n"
            embed.add_field(name="Random", value=randomCommands, inline=False)
            
        await ctx.send(embed=embed)
    
    
    
def setup(bot):
    bot.add_cog(Help(bot))