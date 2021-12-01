import discord
import json
from .managecommands import perms
from discord import member
from discord.utils import get
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
import time
import os
import pymongo as pm


class Reactionroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



# Reaction roles

    @commands.command(pass_context=True, aliases=['r'])
    @commands.has_permissions(manage_roles=True)
    @commands.check(perms)
    async def reactionroles(self, ctx):
        try:
            role_id = int(str(ctx.message.content).split(" ")[1][3:-1])
        except:
            await ctx.reply("you forgot the role variable, format: grear @role emoji text. OBS spaces")
            return
        try:
            emoji = str(ctx.message.content).split(" ")[2]
        except:
            await ctx.reply("you forgot the amoji variable, format: grear @role emoji text. OBS spaces")
            return
        try:
            text = str(ctx.message.content).split(" ")[3:]
        except:
            await ctx.reply("you forgot the text variable, format: grear @role emoji text. OBS spaces")
            return
        highest_role = ctx.message.author.roles[-1]
        role = get(ctx.guild.roles, id=role_id)
        for roles in ctx.guild.roles:
            if role == roles:
                break
            elif highest_role == roles:
                return
        phrase = ""
        for word in text:
            phrase = phrase+" "+word
        message = "Role: "+str(role) + " |" + phrase

        bot_message = await ctx.send(message)
        await bot_message.add_reaction(emoji)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(
            message.reactions, emoji=payload.emoji.name)
        guild = self.bot.get_guild(payload.guild_id)
        if message.author == guild.get_member(self.bot.user.id) and "Role:" == str(message.content)[0:5] and payload.member != guild.get_member(self.bot.user.id):
            role = str(message.content)[6:].split(" |")[0]
            role = discord.utils.get(guild.roles, name=role)
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(
            message.reactions, emoji=payload.emoji.name)
        guild = self.bot.get_guild(payload.guild_id)
        if message.author == guild.get_member(self.bot.user.id) and "Role:" == str(message.content)[0:5]:
            role = str(message.content)[6:].split(" |")[0]
            role = discord.utils.get(guild.roles, name=role)
            member = await guild.fetch_member(payload.user_id)
            await member.remove_roles(role)

    @commands.command(pass_context=True, aliases=['c'])
    @commands.check(perms)
    async def reactionrolesclean(self, ctx):
        await ctx.message.delete()
        channel = ctx.message.channel
        messages = await channel.history(limit=200).flatten()
        tosend = []
        for message in messages:
            if message.content[0:6] == "Role: " and message.author == ctx.guild.get_member(self.bot.user.id) and message.reactions != []:
                tosend.insert(0, {"content": message.content,
                                  "reaction": message.reactions[0]})
                await message.delete()
        for sending in tosend:
            msg = await ctx.send(sending["content"])
            await msg.add_reaction(sending["reaction"])


def setup(bot):
    bot.add_cog(Reactionroles(bot))
