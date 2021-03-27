import discord
import json
from discord.ext import commands, tasks
from discord.utils import get


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def newmembers(self, ctx):
        guild = ctx.guild
        for member in guild.members:
            if len(member.roles) == 1:
                message = "user: "+member.name
                await ctx.send(message)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def prime(self, ctx):
        guild = ctx.guild
        for member in ctx.message.mentions:

            role = get(guild.roles, id=802300233103048704)
            await member.add_roles(role)

            role = get(guild.roles, id=802305915491319838)
            await member.remove_roles(role)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def rprime(self, ctx):
        guild = ctx.guild
        for member in ctx.message.mentions:

            role = get(guild.roles, id=802300233103048704)
            await member.remove_roles(role)

            role = get(guild.roles, id=802305915491319838)
            await member.add_roles(role)

    @commands.command(pass_context=True)
    async def color(self, ctx):
        for role in ctx.message.author.roles:
            if str(role)[0] == ";":
                if len(str(ctx.message.content).split(" ")) > 1:
                    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', "#"+str(ctx.message.content).split(" ")[1]):
                        await role.edit(color=int(("0x"+str(ctx.message.content).split(" ")[1]), 16), reason="Testing")
                        await ctx.send("Successfully changed Color of your role")
                        return
                    else:
                        await ctx.send("Colorcode is invalid format:gcolor ffffff")
                        return
                else:
                    await ctx.send("You need to provide a color code like this:gcolor ffffff")
                    return
        await ctx.send("You dont have a role. \nSo I will create a role for you:")
        role_name = ";"+str(ctx.message.author)[0:-5]
        await ctx.send(role_name)
        role = await ctx.guild.create_role(name=role_name)
        await ctx.message.author.add_roles(role)
        await ctx.send("I have also given you the roles you're welcume")

    


def setup(bot):
    bot.add_cog(Base(bot))