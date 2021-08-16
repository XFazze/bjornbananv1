import discord
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import git
import pymongo as pm







class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot












    # Error handler

    @commands.Cog.listener()
    async def on_command_error(self,ctx:commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"Command on cooldown, ready in {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = f"Missing Permissions you are {error.missing_perms}"
        elif isinstance(error, commands.BotMissingPermissions):
            message = f"Missing Permissions the bot are{error.missing_perms}"
        elif isinstance(error, commands.UserInputError):
            message = "UserInputError"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing Required Argument!!!!!{error.param}"
        elif isinstance(error, commands.DisabledCommand):
            message = "Disabled command"
        elif isinstance(error, commands.TooManyArguments):
            message = "Too many arguments were given"
        elif isinstance(error, commands.MaxConcurrencyReached):
            message = "Max concurrency multiverses"
        elif isinstance(error, commands.NotOwner):
            message = "Not owner ha"
        elif isinstance(error, commands.MessageNotFound):
            message = f"Message not found {error.argument}"
        elif isinstance(error, commands.MemberNotFound):
            message = f"Member not found {error.argument}"
        elif isinstance(error, commands.GuildNotFound):
            message = f"Guild not found {error.argument}"
        elif isinstance(error, commands.UserNotFound):
            message = f"User not found {error.argument}"
        elif isinstance(error, commands.ChannelNotFound):
            message = f"Channel not found {error.argument}"
        elif isinstance(error, commands.ChannelNotReadable):
            message = f"Channel not readable {error.argument}"
        elif isinstance(error, commands.EmojiNotFound):
            message = f"Emoji not found {error.argument}"
        elif isinstance(error, commands.RoleNotFound):
            message = f"Role not found {error.argument}"
        elif isinstance(error, commands.NotOwner):
            message = f"Not owner ha"
        elif isinstance(error, commands.MissingRole):
            message = f"Missing role you are {error.missing_role}"
        elif isinstance(error, commands.BotMissingRole):
            message = f"Missing role the bot is{error.missing_role}"
        elif isinstance(error, commands.MissingAnyRole):
            message = f"Missing any roles{error.missing_roles}"
        elif isinstance(error, commands.BotMissingAnyRole):
            message = f"Missing any roles the bot is {error.missing_roles}"
        elif isinstance(error, commands.NSFWChannelRequired):
            message = f"NSFW channel required {error.channel}"
        elif isinstance(error, commands.ExtensionError):
            message = f"Extension error {error.name}"
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            message = "Cog is already loaded"
        elif isinstance(error, commands.ExtensionNotLoaded):
            message = "Extension not found "
        elif isinstance(error, commands.NoEntryPointError):
            message = "No entry oint error"
        elif isinstance(error, commands.ExtensionFailed):
            message = f"Extension failed name {error.name} original {error.original}"
        elif isinstance(error, commands.ExtensionNotFound):
            message = f"Extension not found name {error.name}"
        elif isinstance(error, commands.CommandRegistrationError):
            message = f"Command registration error name {error.name}  alias conlfict {error.name}"
        elif isinstance(error, FileNotFoundError):
            message = error 
        elif isinstance(error, commands.CommandNotFound):
            message = error
        else:
            message = f"Failure {error}"


            
        print(f"[{ctx.guild}#{ctx.channel}] ERROR HAS OCCURED: ", message)
        embed = discord.Embed(title=message, color=0xFD3333)
        await ctx.send(embed=embed)
        #await ctx.message.delete(delay=5)








    # Git

    @commands.command(pass_context=True)
    async def git(self, ctx, action = None):
        if not str(ctx.author) == "mega#2222" and  not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("You're noone")
            return
        
        g = git.cmd.Git("")
        if action == None:
            embed = discord.Embed(title="Specify an action.", color=0xFD3333)
            await ctx.send(embed=embed)
        elif action == "pull":
            s = g.pull()
            embed = discord.Embed(color=0x00FF42)
            embed.add_field(name="Git pull", value=s)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Action does not exists.", color=0xFD3333)
            await ctx.send(embed=embed)








    # Mongo DB

    @commands.command(pass_context=True)
    async def mdbguild(self, ctx):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return
        docs = []
        for guild in self.bot.guilds:
            text_channels = []
            for channel in guild.text_channels:
                if channel.category != None:
                    category = channel.category.name
                    category_id = channel.category_id
                else:
                    category = None
                    category_id = None

                text_channel = {
                    "id": channel.id,
                    "name": channel.name,
                    "category": category_id,
                    "category_id": category_id,

                }
                text_channels.append(text_channel)
            voice_channels = []
            for channel in guild.voice_channels:
                if channel.category != None:
                    category = channel.category.name
                    category_id = channel.category_id
                else:
                    category = None
                    category_id = None
                voice_channel = {
                    "id": channel.id,
                    "name": channel.name,
                    "category": category_id,
                    "category_id": category_id,
                }
                voice_channels.append(voice_channel)

            doc = {"name": guild.name,
                   "id": guild.id,
                   "text_channels": text_channels,
                   "voice_channels": voice_channels}
            docs.append(doc)

        db  = MongoClient('localhost', 27017).maindb
        collection = db.guilds
        collection.insert_many(docs)

    @commands.command(pass_context=True)
    async def mdbaddconfig(self, ctx):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        db = MongoClient('localhost', 27017).maindb
        collection = db.guilds
        for guild in self.bot.guilds:
            myquery = {"id" : guild.id}
            newvalues = {"$set" : {"config": {
                       "joinrole": [],
                       "prefix": ',',
                       "bettervc": [],
                       "delete_pinned": [],
                       "deletingchannel": [],
                   }}}
            doc = collection.update_one(myquery, newvalues)
            print("doc", doc)








    # Presence

    @commands.command(pass_context=True)
    async def presence(self, ctx, presence = None):
        if not str(ctx.author) == "mega#2222" and  not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return
        await ctx.message.delete()
            
        if presence == None:
            await ctx.send("Specify a presence")
        else:
            await self.bot.change_presence(activity=discord.Game(name=presence))
            await ctx.send("Success")























def setup(bot):
    bot.add_cog(Dev(bot))