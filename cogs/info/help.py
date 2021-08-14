import discord
from discord.ext import commands

import os



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, aliases=['h','commands'])
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="More information about usage is found on:\nhttps://fabbe90.gq/bjornbanan/commands\n\nPrefix: **n.**", color=0xFFFFFF)

        if len(os.listdir('./commands/admin')) > 1:
            adminCommands = ""
            for f in os.listdir('./commands/admin'):
                if f.endswith('.py'):
                    adminCommands += f"> {f[:-3]}\n"
            embed.add_field(name="Admin", value=adminCommands, inline=True)
        
        if len(os.listdir('./commands/moderation')) > 1:
            moderationCommands = ""
            for f in os.listdir('./commands/moderation'):
                if f.endswith('.py'):
                    moderationCommands += f"> {f[:-3]}\n"
            embed.add_field(name="Moderation", value=moderationCommands, inline=True)
        
        if len(os.listdir('./commands/info')) > 1:
            infoCommands = ""
            for f in os.listdir('./commands/info'):
                if f.endswith('.py'):
                    infoCommands += f"> {f[:-3]}\n"
            embed.add_field(name="Info", value=infoCommands, inline=True)
            
        if len(os.listdir('./commands/voice')) > 1:
            voiceCommands = ""
            for f in os.listdir('./commands/voice'):
                if f.endswith('.py'):
                    voiceCommands += f"> {f[:-3]}\n"
            embed.add_field(name="Voice", value=voiceCommands, inline=True)
            
        if len(os.listdir('./commands/logging')) > 1:
            loggingCommands = ""
            for f in os.listdir('./commands/logging'):
                if f.endswith('.py'):
                    loggingCommands += f"> {f[:-3]}\n"
            embed.add_field(name="Logging", value=loggingCommands, inline=True)
            
        if len(os.listdir('./commands/random')) > 1:
            randomCommands = ""
            for f in os.listdir('./commands/random'):
                if f.endswith('.py'):
                    randomCommands += f"> {f[:-3]}\n"
            embed.add_field(name="Random", value=randomCommands, inline=True)
            
        await ctx.send(embed=embed)
    
    
    
def setup(bot):
    bot.add_cog(Help(bot))