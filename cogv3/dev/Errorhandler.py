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


class Errorhandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Errorhandler

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
            collection = MongoClient('localhost', 27017).maindb.errors
            collection.insert_one({
                "errortype" : "MissingRequiredArgument",
                "args" : error.param})
        elif isinstance(error, commands.DisabledCommand):
            message = "Disabled command"
            collection = MongoClient('localhost', 27017).maindb.errors
            collection.insert_one({
                "errortype" : "DisabledCommand",
                "args" : False})
        elif isinstance(error, commands.TooManyArguments):
            collection = MongoClient('localhost', 27017).maindb.errors
            collection.insert_one({
                "errortype" : "TooManyArguments",
                "args" : error.args})
            message = f"Too Many Arguments args: {error.args}"
        elif isinstance(error, commands.MaxConcurrencyReached):
            message = f"Max Concurrency Reached number: {error.number}  per: {error.per}"
        elif isinstance(error, commands.NotOwner):
            message = "Not owner ha"
        elif isinstance(error, commands.MessageNotFound):
            message = f"Message not found {error.argument}"
        elif isinstance(error, commands.MemberNotFound):
            message = f"Member not found {error.argument}"
       # elif isinstance(error, commands.GuildNotFound):
       #     message = f"Guild not found {error.argument}"
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
            collection = MongoClient('localhost', 27017).maindb.errors
            collection.insert_one({
                "errortype" : "NSFWChannelRequired",
                "args" : error.channel})
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
            collection = MongoClient('localhost', 27017).maindb.errors
            collection.insert_one({
                "errortype" : "ConversionError",
                "args" : [error.converter,error.original] })
        elif isinstance(error, commands.ArgumentParsingError):
            message = f"Argument parsing error"
            collection = MongoClient('localhost', 27017).maindb.errors
            collection.insert_one({
                "errortype" : "ArgumentParsingError",
                "args" : False})
        elif isinstance(error, commands.UnexpectedQuoteError):
            message = f"Unexpected quote error quote: {error.quote}"
            collection = MongoClient('localhost', 27017).maindb.errors
            collection.insert_one({
                "errortype" : "UnexpectedQuoteError",
                "args" : error.quote})
        elif isinstance(error, commands.InvalidEndOfQuotedStringError):
            message = f"Invalid end of quoted string error char: {error.char}"
        elif isinstance(error, commands.ExpectedClosingQuoteError):
            message = f"Expected Closing Quote Error close_quote: {error.close_quote}"
            collection = MongoClient('localhost', 27017).maindb.errors
            collection.insert_one({
                "errortype" : "ExpectedClosingQuoteError",
                "args" : error.close_quote})
        elif isinstance(error, commands.BadArgument):
            message = f"Bad Argument args: {error.args}"
            collection = MongoClient('localhost', 27017).maindb.errors
            collection.insert_one({
                "errortype" : "BadArgument",
                "args" : error.args})
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
            collection = MongoClient('localhost', 27017).maindb.errors
            collection.insert_one({
                "errortype" : "CheckAnyFailure",
                "args" : [error.errors, error.checks]})
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




def setup(bot):
    bot.add_cog(Errorhandler(bot))
