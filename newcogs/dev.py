from re import L
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
        self.mdbguildloop.start()


# Error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"Command on cooldown, ready in {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = f"Missing Permissions you are {error.missing_perms}"
        elif isinstance(error, commands.BotMissingPermissions):
            message = f"Missing Permissions the bot are{error.missing_perms}"
        elif isinstance(error, commands.UserInputError):
            message = f"User Input Error args: {error.args}"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing Required Argument!!!!!{error.param}"
        elif isinstance(error, commands.DisabledCommand):
            message = "Disabled command"
        elif isinstance(error, commands.TooManyArguments):
            message = f"Too Many Arguments args: {error.args}"
        elif isinstance(error, commands.MaxConcurrencyReached):
            message = f"Max Concurrency Reached number: {error.number}  per: {error.per}"
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
            message = f"Not owner args: {error.args}"
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
            message = f"Extension error name: {error.name}"
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            message = f"Cog is already loaded name: {error.name}"
        elif isinstance(error, commands.ExtensionNotLoaded):
            message = f"Extension not found name: {error.name}"
        elif isinstance(error, commands.NoEntryPointError):
            message = f"No entry point error name: {error.name}"
        elif isinstance(error, commands.ExtensionFailed):
            message = f"Extension failed name {error.name} original {error.original}"
        elif isinstance(error, commands.ExtensionNotFound):
            message = f"Extension not found name: {error.name}  orignial: {error.original}"
        elif isinstance(error, commands.CommandRegistrationError):
            message = f"Command registration error name {error.name}  alias conlfict {error.name}"
        elif isinstance(error, FileNotFoundError):
            message = error
        elif isinstance(error, commands.ConversionError):
            message = f"ConversionError converter: {error.converter} orignial: {error.original}"
        elif isinstance(error, commands.ArgumentParsingError):
            message = f"Argument parsing error"
        elif isinstance(error, commands.UnexpectedQuoteError):
            message = f"Unexpected quote error quote: {error.quote}"
        elif isinstance(error, commands.InvalidEndOfQuotedStringError):
            message = f"Invalid end of quoted string error char: {error.char}"
        elif isinstance(error, commands.ExpectedClosingQuoteError):
            message = f"Expected Closing Quote Error close_quote: {error.close_quote}"
        elif isinstance(error, commands.BadArgument):
            message = f"Bad Argument args: {error.args}"
        elif isinstance(error, commands.BadUnionArgument):
            message = f"Bad Union Argument param: {error.param}  converters: {error.converters}  errors: {error.errors}"
        elif isinstance(error, commands.PrivateMessageOnly):
            message = f"Private Message Only"
        elif isinstance(error, commands.NoPrivateMessage):
            message = f"No Private Message"
        elif isinstance(error, commands.CheckFailure):
            message = f"Check Failure"
        elif isinstance(error, commands.CheckAnyFailure):
            message = f"Check Any Failure errors: {error.errors}  checks: {error.checks}"
        elif isinstance(error, commands.CommandInvokeError):
            message = f"Command Invoke Error original: {error.original}"
        elif isinstance(error, commands.BadColourArgument):
            message = f"Bad Colour Argument argument: {error.argument}"
        elif isinstance(error, commands.BadInviteArgument):
            message = f"Bad Invite Argument"
        elif isinstance(error, commands.PartialEmojiConversionFailure):
            message = f"Partial Emoji Conversion Failure argument: {error.argument}"
        elif isinstance(error, commands.BadBoolArgument):
            message = f"Bad Bool Argument argument: {error.argument}"
        else:
            message = f"Failure {error}"

        print(f"[{ctx.guild}#{ctx.channel}] ERROR HAS OCCURED: ", message)
        embed = discord.Embed(title=message, color=0xFD3333)
        await ctx.send(embed=embed)
        # await ctx.message.delete(delay=5)


# Rate limited
    @commands.Cog.listener()
    async def is_ws_ratelimited(self):
        print("Being websocket ratelimited")


# Git
    @commands.command(pass_context=True)
    async def git(self, ctx, action=None):
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
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
            embed = discord.Embed(
                title="Action does not exists.", color=0xFD3333)
            await ctx.send(embed=embed)


# Mongo DB
    @commands.command(pass_context=True)
    async def mdbguildupdate(self):
        db = MongoClient('localhost', 27017).maindb
        collection = db.guilds

        for guild in self.bot.guilds:
            myquery = {"id": guild.id}
            doc = collection.find_one(myquery)
            create = False
            if doc == None:
                create = True
                doc = {
                    "id": guild.id,
                    "name": guild.name
                }

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


            doc["text_channels"] = text_channels
            doc["voice_channels"] = voice_channels
            if "config" not in doc.keys():
                doc["config"] = {}
            if "joinrole" not in doc["config"].keys():
                doc["config"]["joinrole"] = []
            if "prefix" not in doc["config"].keys():
                doc["config"]["prefix"] = ','
            if "bettervc" not in doc["config"].keys():
                doc["config"]["bettervc"] = []
            if "delete_pinned" not in doc["config"].keys():
                doc["config"]["delete_pinned"] = []
            if "deletingchannel" not in doc["config"].keys():
                doc["config"]["deletingchannel"] = []
            if "joinleavemessage" not in doc["config"].keys():
                doc["config"]["joinleavemessage"] = []

            if "settings" not in doc.keys():
                doc["settings"] = {}

            if create:
                collection.insert_one(doc)
            else:
                myquery = {"id": guild.id}
                collection.replace_one(myquery, doc)

    @commands.command(pass_context=True)
    async def dmdbguild(self, ctx):
        await ctx.message.delete()
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return
        await self.mdbguildupdate()
        await ctx.send(embed=discord.Embed(title="Successfully updated mongodbguild", color=0x00FF42))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.mdbguildupdate()
        
    @tasks.loop(seconds=120) 
    async def mdbguildloop(self):
        await self.mdbguildupdate()
        
       
    @mdbguildloop.before_loop
    async def before_cleanse(self):
        print('deletingchannel enabled')
        await self.bot.wait_until_ready()


# Presence
    @commands.command(pass_context=True)
    async def presence(self, ctx, presence=None):
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return
        await ctx.message.delete()

        if presence == None:
            await ctx.send("Specify a presence")
        else:
            await self.bot.change_presence(activity=discord.Game(name=presence))
            await ctx.send("Success")


# Activity      OBS!   W.I.P
    @commands.command(pass_context=True, aliases=[], usage="activity [activity]")
    async def activity(self, ctx, activity=None):
        if not str(ctx.author) == "mega#2222" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.send("Youre noone")
            return

        if activity == None:
            embed = discord.Embed(title=f'Usage: `{self.bot.get_command("activity").usage}`', color=0xFD3333)
            await ctx.send(embed=embed)
        else:
            custom_activity = discord.Activity(name=activity, type=5)
            await self.bot.change_presence(activity=custom_activity)
            embed = discord.Embed(title=f'Tried to set activity: `{activity}`', color=0x00FF42)
            await ctx.send(embed=embed)





def setup(bot):
    bot.add_cog(Dev(bot))
