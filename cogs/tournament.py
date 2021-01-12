import discord
import json
from discord.ext import commands
from discord.utils import get


class Base(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        laglos = "insert id here"
        lagkapten = "insert id here"

    @commands.command(pass_context=True, aliases=['.create'])
    async def create_team(self,ctx):
        f = json.load(open("servers.json", "r"))
        if str(ctx.message.guild.id) not in f[".create"]:
            print("not allowed on server")
            await ctx.send("COMMAND NOT ALLOWED IN YOUR HOME")
            return

        author = ctx.message.author
        guild = ctx.guild
        roleid = get(guild.roles, id=lagkapten)
        await author.add_roles(roleid)
        mentions = ctx.message.mentions
        mentions.append(author)
        role_name = author.display_name
        role = await guild.create_role(hoist=True, mentionable=True, name=role_name, colour=discord.Colour(0x0000FF))
        roleid = get(guild.roles, id=laglos)
        for people in mentions:
            await people.remove_roles(roleid)
            await people.add_roles(role)


    @commands.command(pass_context=True, aliases=['.skapa_kanaler'])
    async def create_channels(self,ctx):
        f = json.load(open("servers.json", "r"))
        if str(ctx.message.guild.id) not in f[".skapa_kanaler"]:
            print("not allowed on server")
            await ctx.send("COMMAND NOT ALLOWED IN YOUR HOME")
            return
        author = ctx.message.author
        teamrole = author.roles[1]
        guild = ctx.guild
        name = teamrole.name
        category = await guild.create_category(name=name)
        everyone_role = guild.default_role
        await category.set_permissions(everyone_role, read_messages=False)
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = True
        await category.set_permissions(teamrole, overwrite=overwrite)
        await guild.create_text_channel(name=name+"text", category=category)
        await guild.create_voice_channel(name=name+"voice", category=category)

def setup(bot):
    bot.add_cog(Base(bot))