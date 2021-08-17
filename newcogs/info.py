import discord, datetime, time
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import random


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Help
    
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
   

# User info
    
    @commands.command(pass_context=True, aliases= ['userinfo'])
    async def user(self, ctx, member:discord.Member = None):
        
        await ctx.message.delete()
        
        if member is None:
            
            roles_list = ' | '.join(map(str, ctx.author.roles))
            
            embed=discord.Embed(title=member, color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="ID", value=ctx.author.id, inline=False)
            embed.add_field(name="Nickname", value=ctx.author.nick, inline=False)
            embed.add_field(name="Highest role", value=ctx.author.top_role, inline=False)
            embed.add_field(name="Roles", value=roles_list, inline=False)
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        
        
        else:
            
            roles_list = ' | '.join(map(str, member.roles))
            
            embed=discord.Embed(title=member, color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="ID", value=member.id, inline=False)
            embed.add_field(name="Nickname", value=member.nick, inline=False)
            embed.add_field(name="Highest role", value=member.top_role, inline=False)
            embed.add_field(name="Roles", value=roles_list, inline=False)
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)
    
    
    @commands.command(pass_context=True, aliases=['av'])
    async def avatar(self, ctx, member:discord.Member = None):
        
        await ctx.message.delete()
        if member is None:
            
            embed=discord.Embed(title=ctx.author, color=random.randint(0, 0xFFFFFF))
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        
        
        else:
            
            embed=discord.Embed(title=member, color=random.randint(0, 0xFFFFFF))
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)
     
    
# Server info
    
    @commands.command(pass_context=True, aliases=['serverinfo', 'guild'])
    async def server(self, ctx):
        await ctx.message.delete()
        
        
        embed=discord.Embed(title=ctx.guild, color=random.randint(0, 0xFFFFFF))
        embed.add_field(name="Owner", value=ctx.guild.owner, inline=False)
        embed.add_field(name="ID", value=ctx.guild.id, inline=False)
        embed.add_field(name="Member count", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Creation Date", value=ctx.guild.created_at, inline=False)
        embed.add_field(name="Region", value=ctx.guild.region, inline=False)
        embed.add_field(name="Number of text channels", value=len(ctx.guild.text_channels), inline=False)
        embed.add_field(name="Number of voice channels", value=len(ctx.guild.voice_channels), inline=False)
        embed.add_field(name="Number of categories", value=len(ctx.guild.categories), inline=False)
        
        
        embed.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
    
# Bot info
    @commands.command(pass_context=True, aliases=['botinfo', 'bot'])
    async def appinfo(self, ctx):
        res = await self.bot.application_info()
        embed=discord.Embed(title=res.name, description=res.description, color=0x00FF42)
        if res.bot_public:
            embed.add_field(name="Public bot Owner:", value=res.owner.name+"#"+res.owner.discriminator)
        else:
            embed.add_field(name="Private bot Owner: ", value=res.owner.name+"#"+res.owner.discriminator)
        embed.add_field(name='Id', value=res.id, inline=False)
        embed.add_field(name='Guilds', value=len(self.bot.guilds), inline=False)
        embed.add_field(name='Users', value=len(self.bot.users), inline=False)
        embed.add_field(name='Commands', value=len(self.bot.commands), inline=False)
        embed.add_field(name='Emojis', value=len(self.bot.emojis), inline=False)
        embed.add_field(name='Latency', value=self.bot.latency*1000, inline=False)
        embed.add_field(name='Private channels', value=len(self.bot.private_channels), inline=False)
        embed.add_field(name='Voice clients', value=len(self.bot.voice_clients), inline=False)
        await ctx.send(embed=embed)
# Ping
    
    @commands.command(pass_context=True, aliases=['latency'])
    async def ping(self, ctx):
        
        #await ctx.message.delete()
        embed = discord.Embed(colour=0xFFFFFF)
        embed.add_field(name="Latency", value='{0}ms'.format(round(self.bot.latency*1000, 1)))
        await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(Info(bot))