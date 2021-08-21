import discord
from ..admin.managecommands import perms
import json
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
from discord.utils import get
import time
import os
import pymongo as pm


class Rolelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Role log

    @commands.command(pass_context=True, aliases=['er'])
    @commands.has_permissions(manage_roles=True)
    @commands.check(perms)
    async def enablerolelog(self, ctx):
        with open('/tmp/discordbot/management/rolelog.json', 'r+') as f:
            rolelog = json.load(f)
            c_id = ctx.channel.id
            g_id = str(ctx.guild.id)
            if c_id in rolelog.values():
                await ctx.send("This channel is already added to rolelog")
            else:
                rolelog[g_id] = c_id
                await ctx.send("Added channel to rolelog")
                with open('/tmp/discordbot/management/rolelog.json', 'w') as file:
                    json.dump(rolelog, file, indent=4)

    @commands.command(pass_context=True, aliases=['dr'])
    @commands.has_permissions(manage_roles=True)
    @commands.check(perms)
    async def disablerolelog(self, ctx):
        with open('/tmp/discordbot/management/rolelog.json', 'r+') as f:
            rolelog = json.load(f)
            c_id = ctx.channel.id
            g_id = str(ctx.guild.id)
            if c_id in rolelog.values():
                del rolelog[g_id]
                await ctx.send("removed channel to rolelog")
                with open('/tmp/discordbot/management/rolelog.json', 'w') as file:
                    json.dump(rolelog, file, indent=4)
            else:
                await ctx.send("This channel isnta a rolelog channel")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles == after.roles:
            return
        else:
            with open('/tmp/discordbot/management/rolelog.json', 'r') as f:
                rolelog = json.load(f)
                guild_id = str(before.guild.id)
                if guild_id not in rolelog.keys():
                    return
                channel_id = rolelog[guild_id]
                channel = self.bot.get_channel(channel_id)
                if len(before.roles) > len(after.roles):
                    role = list(set(before.roles)-set(after.roles))[0]
                    message = "User: " + \
                        str(before) + "\nRole removed: " + role.name
                    await channel.send(message)
                else:
                    role = list(set(after.roles)-set(before.roles))[0]
                    if role.id == 802300001875001455:
                        message = "@everyone User: " + \
                            str(before) + "\nRole added: " + role.name
                    else:
                        message = "User: " + \
                            str(before) + "\nRole added: " + role.name
                    await channel.send(message)



def setup(bot):
    bot.add_cog(Rolelog(bot))
