import discord
from discord.ext import commands
import os


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, aliases=['h','commands'])
    async def help(self, ctx):
        
        await ctx.message.delete()
        embed = discord.Embed(title="Help", description="More information about usage is found on:\nhttps://fabbe90.gq/bjornbanan/commands\n\nPrefix: **,**", color=0xFFFFFF)

        if len(os.listdir('./cogs/admin')) > 1:
            adminCommands = ""
            for f in os.listdir('./cogs/admin'):
                if f.endswith('.py'):
                    adminCommands += f"> {f[:-3]}\n"
            for f in os.listdir('./cogs/admin/channels'):
                if f.endswith('.py'):
                    adminCommands += f"> {f[:-3]}\n"
            embed.add_field(name="Admin", value=adminCommands, inline=True)
        
        if len(os.listdir('./cogs/moderation')) > 1:
            moderationCommands = ""
            for f in os.listdir('./cogs/moderation'):
                if f.endswith('.py'):
                    moderationCommands += f"> {f[:-3]}\n"
            embed.add_field(name="Moderation", value=moderationCommands, inline=True)
        
        if len(os.listdir('./cogs/info')) > 1:
            infoCommands = ""
            for f in os.listdir('./cogs/info'):
                if f.endswith('.py'):
                    infoCommands += f"> {f[:-3]}\n"
            embed.add_field(name="Info", value=infoCommands, inline=True)
            
        if len(os.listdir('./cogs/voice')) > 1:
            voiceCommands = ""
            for f in os.listdir('./cogs/voice'):
                if f.endswith('.py'):
                    voiceCommands += f"> {f[:-3]}\n"
            embed.add_field(name="Voice", value=voiceCommands, inline=True)
            
        if len(os.listdir('./cogs/stats')) > 1:
            statsCommands = ""
            for f in os.listdir('./cogs/stats'):
                if f.endswith('.py'):
                    statsCommands += f"> {f[:-3]}\n" 
            embed.add_field(name="Stats", value=statsCommands, inline=True)
            
        if len(os.listdir('./cogs/utilities')) > 1:
            utilitiesCommands = ""
            for f in os.listdir('./cogs/utilities'):
                if f.endswith('.py'):
                    utilitiesCommands += f"> {f[:-3]}\n"
            embed.add_field(name="Utilities", value=utilitiesCommands, inline=True)
            
        await ctx.send(embed=embed)
    
    
    
def setup(bot):
    bot.add_cog(Help(bot))