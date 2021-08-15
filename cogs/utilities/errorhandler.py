import discord
import json
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            message = "Extension already loaded"
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
        else:
            message = "Oh no! Something went wrong while running the command!"


            
        print("ERROR HAS UCCURED", message)
        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)


def setup(bot):
    bot.add_cog(Base(bot))