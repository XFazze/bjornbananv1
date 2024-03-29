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


class Presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



# presence

    @commands.command(pass_context=True, aliases=[], usage="activity [activity]", hidden=True)
    async def presence(self, ctx, activity=None, type: int = None):
        if not str(ctx.author) == "mega#5630" and not str(ctx.author) == "AbstractNucleus#6969":
            await ctx.reply("Youre noone")
            return

        if activity == None or type == None:
            embed = discord.Embed(
                title=f'Usage: `{self.bot.get_command("activity").usage}`', color=0xFD3333)
            await ctx.reply(embed=embed)
        else:
            custom_activity = discord.Activity(name=activity, type=type)
            await self.bot.change_presence(activity=custom_activity)
            embed = discord.Embed(
                title=f'Tried to set activity: `{activity}`', color=0x00FF42)
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Presence(bot))
