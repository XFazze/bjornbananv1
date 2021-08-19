import discord
from discord import embeds
from discord.ext import commands
from discord.ext.commands.core import command
from pymongo import MongoClient, collation
from discord_components import Button, Select, SelectOption, ComponentsBot
from discord.utils import get


class managecommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Enable/disable command

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx, command: str = None, role: discord.Role = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break
        if not validcommand:
            await ctx.send(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
            return

        if role == None:
            role = ctx.guild.default_role

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        settings = collection.find_one(myquery)["settings"]
        if command not in settings.keys():
            settings[command] = {
                "guild": [],
                "disabled_guild":  [],
                "category":  {},
                "disabled_category": {},
                "channel":  {},
                "disabled_channel":  {}
            }

        if role.id not in settings[command]['disabled_guild']:
            settings[command]['disabled_guild'].append(role.id)
        else:
            await ctx.send(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))
            return

        if role.id in settings[command]['guild']:
            settings[command]['guild'].remove(role.id)
        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.send(embed=discord.Embed(title="Disabled "+command+" on server for "+role.name, color=0x00FF42))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def disablecategory(self, ctx, category: discord.CategoryChannel = None, command: str = None, role: discord.Role = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break

        if not validcommand:
            await ctx.send(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
            return

        if role == None:
            role = ctx.guild.default_role

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        settings = collection.find_one(myquery)["settings"]
        if command not in settings.keys():
            settings[command] = {
                "guild": [],
                "disabled_guild":  [],
                "category":  {},
                "disabled_category": {},
                "channel":  {},
                "disabled_channel":  {}
            }

        if str(category.id) not in settings[command]['disabled_category'].keys():
            settings[command]['disabled_category'][str(category.id)] = [
                role.id]

        else:
            if role.id in settings[command]['disabled_category'][str(category.id)]:
                await ctx.send(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))
                return
            else:
                settings[command]['disabled_category'][str(
                    category.id)].append(role.id)

        if str(category.id) in settings[command]['category'].keys():
            if role.id in settings[command]['category'][str(category.id)]:
                settings[command]['category'][str(category.id)].remove(role.id)

        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.send(embed=discord.Embed(title="Disabled "+command+" in category " + category.name+" for "+role.name + category.name, color=0x00FF42))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def disablechannel(self, ctx, channel: discord.TextChannel = None, command: str = None, role: discord.Role = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break

        if not validcommand:
            await ctx.send(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
            return

        if role == None:
            role = ctx.guild.default_role

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        settings = collection.find_one(myquery)["settings"]
        if command not in settings.keys():
            settings[command] = {
                "guild": [],
                "disabled_guild":  [],
                "category":  {},
                "disabled_category": {},
                "channel":  {},
                "disabled_channel":  {}
            }

        if str(channel.id) not in settings[command]['disabled_channel'].keys():
            settings[command]['disabled_channel'][str(channel.id)] = [role.id]

        else:
            if role.id in settings[command]['disabled_channel'][str(channel.id)]:
                await ctx.send(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))
                return
            else:
                settings[command]['disabled_channel'][str(
                    channel.id)].append(role.id)

        if str(channel.id) in settings[command]['channel'].keys():
            if role.id in settings[command]['channel'][str(channel.id)]:
                settings[command]['channel'][str(channel.id)].remove(role.id)

        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.send(embed=discord.Embed(title="Disabled "+command+" in channel " + channel.name+" for "+role.name, color=0x00FF42))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx, command: str = None, role: discord.Role = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break
        if not validcommand:
            await ctx.send(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
            return

        if role == None:
            role = ctx.guild.default_role

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        settings = collection.find_one(myquery)["settings"]
        if command not in settings.keys():
            settings[command] = {
                "guild": [],
                "disabled_guild":  [],
                "category":  {},
                "disabled_category": {},
                "channel":  {},
                "disabled_channel":  {}
            }

        if role.id not in settings[command]['guild']:
            settings[command]['guild'].append(role.id)
        else:
            await ctx.send(embed=discord.Embed(title="Command is already enabled", color=0xFD3333))
            return

        if role.id in settings[command]['disabled_guild']:
            settings[command]['disabled_guild'].remove(role.id)

        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.send(embed=discord.Embed(title="Enabled "+command+" on server for "+role.name, color=0x00FF42))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def enablecategory(self, ctx, category: discord.CategoryChannel = None, command: str = None, role: discord.Role = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break

        if not validcommand:
            await ctx.send(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
            return

        if role == None:
            role = ctx.guild.default_role

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        settings = collection.find_one(myquery)["settings"]
        if command not in settings.keys():
            settings[command] = {
                "guild": [],
                "disabled_guild":  [],
                "category":  {},
                "disabled_category": {},
                "channel":  {},
                "disabled_channel":  {}
            }

        if str(category.id) not in settings[command]['category'].keys():
            settings[command]['category'][str(category.id)] = [role.id]

        else:
            if role.id in settings[command]['category'][str(category.id)]:
                await ctx.send(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))
                return
            else:
                settings[command]['category'][str(category.id)].append(role.id)

        if str(category.id) in settings[command]['disabled_category'].keys():
            if role.id in settings[command]['disabled_category'][str(category.id)]:
                settings[command]['disabled_category'][str(
                    category.id)].remove(role.id)

        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.send(embed=discord.Embed(title="Enabled "+command+" in category " + category.name + " for "+role.name, color=0x00FF42))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def enablechannel(self, ctx, channel: discord.TextChannel = None, command: str = None, role: discord.Role = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break

        if not validcommand:
            await ctx.send(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
            return

        if role == None:
            role = ctx.guild.default_role

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        settings = collection.find_one(myquery)["settings"]
        if command not in settings.keys():
            settings[command] = {
                "guild": [],
                "disabled_guild":  [],
                "category":  {},
                "disabled_category": {},
                "channel":  {},
                "disabled_channel":  {}
            }

        if str(channel.id) not in settings[command]['channel'].keys():
            settings[command]['channel'][str(channel.id)] = [role.id]

        else:
            if role.id in settings[command]['channel'][str(channel.id)]:
                await ctx.send(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))
                return
            else:
                settings[command]['channel'][str(channel.id)].append(role.id)

        if str(channel.id) in settings[command]['disabled_channel'].keys():
            if role.id in settings[command]['disabled_channel'][str(channel.id)]:
                settings[command]['disabled_channel'][str(
                    channel.id)].remove(role.id)

        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.send(embed=discord.Embed(title="Enabled "+command+" in channel " + channel.name + " for "+role.name, color=0x00FF42))

    @commands.command(pass_context=True)
    async def command(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        settings = collection.find_one(myquery)["settings"]
        options=[]
        for setting in settings.keys():
            options.append(SelectOption(label=setting, value=setting))

        message = await ctx.send("NOEEEL", components=[Select(placeholder="Select something!", options=options, custom_id="commandperms",)])
        while True:
            interaction = await self.bot.wait_for("select_option")
            embed = discord.Embed(name="Command permissions for ", value=interaction.values[0])
            if len(settings[interaction.values[0]]["guild"]) > 0:
                msg = ""
                for roleid in settings[interaction.values[0]]["guild"]:
                    role_obj = get(ctx.guild.roles, id=roleid)
                    msg += role_obj.name+'\n'
            embed.add_field(name="GUILD WIDE allowed", value=msg)
            if len(settings[interaction.values[0]]["guild"]) > 0:
                msg = ""
                for roleid in settings[interaction.values[0]]["disabled_guild"]:
                    role_obj = get(ctx.guild.roles, id=roleid)
                    msg += role_obj.name+'\n'
            embed.add_field(name="GUILD WIDE denied", value=msg)


                
            await message.edit(embed=embed,components=[Select(placeholder="Select something!", options=options, custom_id="commandperms",)])



def setup(bot):
    bot.add_cog(managecommands(bot))
