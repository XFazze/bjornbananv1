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
            await ctx.reply(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
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
            await ctx.reply(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))
            return

        if role.id in settings[command]['guild']:
            settings[command]['guild'].remove(role.id)
        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.reply(embed=discord.Embed(title="Disabled "+command+" on server for "+role.name, color=0x00FF42))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def disablecategory(self, ctx, category: discord.CategoryChannel = None, command: str = None, role: discord.Role = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break

        if not validcommand:
            await ctx.reply(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
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
                await ctx.reply(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))
                return
            else:
                settings[command]['disabled_category'][str(
                    category.id)].append(role.id)

        if str(category.id) in settings[command]['category'].keys():
            if role.id in settings[command]['category'][str(category.id)]:
                settings[command]['category'][str(category.id)].remove(role.id)

        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.reply(embed=discord.Embed(title="Disabled "+command+" in category " + category.name+" for "+role.name + category.name, color=0x00FF42))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def disablechannel(self, ctx, channel: discord.TextChannel = None, command: str = None, role: discord.Role = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break

        if not validcommand:
            await ctx.reply(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
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
                await ctx.reply(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))
                return
            else:
                settings[command]['disabled_channel'][str(
                    channel.id)].append(role.id)

        if str(channel.id) in settings[command]['channel'].keys():
            if role.id in settings[command]['channel'][str(channel.id)]:
                settings[command]['channel'][str(channel.id)].remove(role.id)

        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.reply(embed=discord.Embed(title="Disabled "+command+" in channel " + channel.name+" for "+role.name, color=0x00FF42))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx, command: str = None, role: discord.Role = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break
        if not validcommand:
            await ctx.reply(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
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
            await ctx.reply(embed=discord.Embed(title="Command is already enabled", color=0xFD3333))
            return

        if role.id in settings[command]['disabled_guild']:
            settings[command]['disabled_guild'].remove(role.id)

        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.reply(embed=discord.Embed(title="Enabled "+command+" on server for "+role.name, color=0x00FF42))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def enablecategory(self, ctx, category: discord.CategoryChannel = None, command: str = None, role: discord.Role = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break

        if not validcommand:
            await ctx.reply(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
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
                await ctx.reply(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))
                return
            else:
                settings[command]['category'][str(category.id)].append(role.id)

        if str(category.id) in settings[command]['disabled_category'].keys():
            if role.id in settings[command]['disabled_category'][str(category.id)]:
                settings[command]['disabled_category'][str(
                    category.id)].remove(role.id)

        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.reply(embed=discord.Embed(title="Enabled "+command+" in category " + category.name + " for "+role.name, color=0x00FF42))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def enablechannel(self, ctx, channel: discord.TextChannel = None, command: str = None, role: discord.Role = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break

        if not validcommand:
            await ctx.reply(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
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
                await ctx.reply(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))
                return
            else:
                settings[command]['channel'][str(channel.id)].append(role.id)

        if str(channel.id) in settings[command]['disabled_channel'].keys():
            if role.id in settings[command]['disabled_channel'][str(channel.id)]:
                settings[command]['disabled_channel'][str(
                    channel.id)].remove(role.id)

        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.reply(embed=discord.Embed(title="Enabled "+command+" in channel " + channel.name + " for "+role.name, color=0x00FF42))
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def resetperms(self, ctx, command: str = None):
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break

        if not validcommand:
            await ctx.reply(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
            return

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        settings = collection.find_one(myquery)["settings"]
        settings[command] = {
            "guild": [],
            "disabled_guild":  [],
            "category":  {},
            "disabled_category": {},
            "channel":  {},
            "disabled_channel":  {}}
            

        newvalue = {"$set": {"settings": settings}}
        collection.update_one(myquery, newvalue)
        await ctx.reply(embed=discord.Embed(title="Reset command permissions", color=0x00FF42))

    @commands.command(pass_context=True)
    async def showperms(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        settings = collection.find_one(myquery)["settings"]
        options=[]
        for setting in settings.keys():
            options.append(SelectOption(label=setting, value=setting))

        message = await ctx.reply("The lower in the hiearchy will go over the other. So channel enable will go over guild disable.", components=[Select(placeholder="Select something!", options=options, custom_id="commandperms",)])
        while True:
            interaction = await self.bot.wait_for("select_option")
            embed = discord.Embed(name="Command permissions for ", value=interaction.values[0], color=0xFFFFFF)

            if len(settings[interaction.values[0]]["guild"]) > 0:
                msg = ""
                for roleid in settings[interaction.values[0]]["guild"]:
                    role_obj = get(ctx.guild.roles, id=roleid)
                    msg += role_obj.name+'\n'
            else:
                msg="None"
            embed.add_field(name="Guild wide allowed", value=msg)
            if len(settings[interaction.values[0]]["guild"]) > 0:
                msg = ""
                for roleid in settings[interaction.values[0]]["disabled_guild"]:
                    role_obj = get(ctx.guild.roles, id=roleid)
                    msg += role_obj.name+'\n'
            else:
                msg="None"
            embed.add_field(name="Guild wide denied", value=msg)



            # this is no longer a list
            # its a dictionary
            embed.add_field(name="Category wide allowed", value="\u200b", inline=False)
            if len(settings[interaction.values[0]]["category"].keys()) > 0:
                for key in settings[interaction.values[0]]["category"].keys():
                    if len(settings[interaction.values[0]]["category"][key]) == 0:
                        continue
                    
                    msg = ""
                    for roleid in settings[interaction.values[0]]["category"][key]:
                        role_obj = get(ctx.guild.roles, id=roleid)
                        msg += role_obj.name+'\n'
                    name = get(ctx.guild.categories, id=int(key))
                    embed.add_field(name=name, value=msg)
            else:
                msg = "None"

            embed.add_field(name="Category wide denied", value="\u200b", inline=False)
            if len(settings[interaction.values[0]]["disabled_category"].keys()) > 0:
                for key in settings[interaction.values[0]]["disabled_category"].keys():
                    if len(settings[interaction.values[0]]["disabled_category"][key]) == 0:
                        continue
                    
                    msg = ""
                    for roleid in settings[interaction.values[0]]["disabled_category"][key]:
                        role_obj = get(ctx.guild.roles, id=roleid)
                        msg += role_obj.name+'\n'
                    name = get(ctx.guild.categories, id=int(key))
                    embed.add_field(name=name, value=msg)
            else:
                msg = "None"



            embed.add_field(name="Channel wide allowed", value="\u200b", inline=False)
            if len(settings[interaction.values[0]]["channel"].keys()) > 0:
                for key in settings[interaction.values[0]]["channel"].keys():
                    if len(settings[interaction.values[0]]["channel"][key]) == 0:
                        continue
                    
                    msg = ""
                    for roleid in settings[interaction.values[0]]["channel"][key]:
                        role_obj = get(ctx.guild.roles, id=roleid)
                        msg += role_obj.name+'\n'
                    name = get(ctx.guild.text_channels, id=int(key))
                    embed.add_field(name=name, value=msg)
            else:
                msg = "None"

            embed.add_field(name="Channel wide denied", value="\u200b", inline=False)
            if len(settings[interaction.values[0]]["disabled_channel"].keys()) > 0:
                for key in settings[interaction.values[0]]["disabled_channel"].keys():
                    if len(settings[interaction.values[0]]["disabled_channel"][key]) == 0:
                        continue
                    
                    msg = ""
                    for roleid in settings[interaction.values[0]]["disabled_channel"][key]:
                        role_obj = get(ctx.guild.roles, id=roleid)
                        msg += role_obj.name+'\n'
                    name = get(ctx.guild.text_channels, id=int(key))
                    embed.add_field(name=name, value=msg)
            else:
                msg = "There "


                
            await message.edit(embed=embed,components=[Select(placeholder="Select something!", options=options, custom_id="commandperms",)])


    


def setup(bot):
    bot.add_cog(managecommands(bot))
    
def perms(context):
        command = context.command.name #str
        guild_id = context.guild.id
        channel_id = str(context.message.channel.id)
        category_id = str(context.message.channel.category_id)
        roles = []
        for role in context.author.roles:
            roles.append(role.id)

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": guild_id}
        settings = collection.find_one(myquery)["settings"]
        if command in settings.keys():
            if channel_id in settings[command]["channel"].keys():
                print("channels exist")
                if bool(set(roles) & set(settings[command]["channel"][channel_id])):
                    return True

            elif channel_id in settings[command]["disabled_channel"].keys():
                if bool(set(roles) & set(settings[command]["disabled_channel"][channel_id])):
                    return False
                    
            elif category_id in settings[command]["category"].keys():
                if bool(set(roles) & set(settings[command]["category"][category_id])):
                    return True
                    
            elif category_id in settings[command]["disabled_category"].keys():
                if bool(set(roles) & set(settings[command]["disabled_category"][category_id])):
                    return False

            elif  bool(set(roles) & set(settings[command]["disabled_guild"])):
                return False

            elif bool(set(roles) & set(settings[command]["guild"])):
                return True
                    

        return True