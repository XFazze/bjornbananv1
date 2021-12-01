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


class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



# Git

    @commands.command(pass_context=True)
    async def git(self, ctx, action=None, hidden=True):
        if not str(ctx.author) == "mega#5630" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.reply("You're noone")
            return

        g = git.cmd.Git("")
        if action == None:
            embed = discord.Embed(title="Specify an action.", color=0xFD3333)
            await ctx.reply(embed=embed)
        elif action == "pull":
            s = g.pull()
            embed = discord.Embed(color=0x00FF42)
            embed.add_field(name="Git pull", value=s)
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="Action does not exists.", color=0xFD3333)
            await ctx.reply(embed=embed)




def setup(bot):
    bot.add_cog(Git(bot))
