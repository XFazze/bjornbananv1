import discord
from ..admin.managecommands import perms
import json
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm
import math
import random
import re
import asyncio


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Clear   
    @commands.command(aliases = ['purge','delete', 'g'], usage="clear [int]")
    @commands.has_permissions(manage_messages = True)
    @commands.check(perms)
    async def clear(self, ctx, amount = None):
        async with ctx.typing():
            if amount == None:
                embed = discord.Embed(title=f'Usage: `{self.bot.get_command("clear").usage}`', color=0xFD3333)
                await ctx.send(embed=embed)
            else:
                try:
                    amount = int(amount)
                    await ctx.channel.purge(limit=amount+1)
                    embed = discord.Embed(title=f'Tried to delete `{amount}` messages')
                    await ctx.send(embed=embed, delete_after=10)
                except:
                    embed = discord.Embed(title=f'Usage: `{self.bot.get_command("clear").usage}`', color=0xFD3333)
                    await ctx.send(embed=embed)
                


def setup(bot):
    bot.add_cog(Clear(bot))