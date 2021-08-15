import discord
import json
import math
import re
import time
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['g', 'purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx):
        await ctx.message.delete()
        try:
            message = ctx.message.content.split(" ")
            amount = int(message[1])
            print(f"asked to delete {amount} messages by {ctx.message.author}")
            await ctx.message.delete()
        except:
            await ctx.send('provide a valid number("gclear 2")')
            return
        try:
            if message[2] == "not":
                try:
                    note = int(message[3])
                except:
                    await ctx.send('You need to provide a number ("gclear x not z" z can be 1 or 5 etc )')
                    return

        except:
            note = 0
        if amount > 99:
            secret = await ctx.send('You executed the secret protocol')
            for x in range(math.floor(amount/99)):
                messages = await ctx.message.channel.history(limit=101+note).flatten()
                for _ in range(note+1):
                    messages.pop(0)
                await ctx.message.channel.delete_messages(messages)
            amount = amount % 99
            await secret.delete()
        messages = await ctx.message.channel.history(limit=amount+note).flatten()
        if note:
            print(len(messages))
            for _ in range(note):
                messages.pop(0)

        await ctx.message.channel.delete_messages(messages)

        message = await ctx.send(f"I have deleted {amount} messages for you master")
        time.sleep(2)
        await message.delete()

def setup(bot):
    bot.add_cog(Base(bot))