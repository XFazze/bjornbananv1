import discord
import json
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['edp'])
    @commands.has_permissions(manage_messages=True)
    async def enabledeletepinned(self, ctx):
        with open('/tmp/discordbot/management/delete_pinned.json', 'r+') as f:
            delete_pinned = json.load(f)
            c_id = ctx.channel.id
            if c_id in delete_pinned:
                await ctx.send("This channel is already added to delete_pinned")
            else:
                delete_pinned.append(c_id)
                await ctx.send("Added channel to delete_pinned")
                with open('/tmp/discordbot/management/delete_pinned.json', 'w') as file:
                    json.dump(delete_pinned, file, indent=4)

    @commands.command(pass_context=True, aliases=['ddp'])
    @commands.has_permissions(manage_messages=True)
    async def disabledeletepinned(self, ctx):
        with open('/tmp/discordbot/management/delete_pinned.json', 'r+') as f:
            delete_pinned = json.load(f)
            c_id = ctx.channel.id
            if c_id in delete_pinned:
                delete_pinned.remove(c_id)
                await ctx.send("removed channel from delete_pinned")
                with open('/tmp/discordbot/management/delete_pinned.json', 'w') as file:
                    json.dump(delete_pinned, file, indent=4)
            else:
                await ctx.send("This channel isnta a delete_pinned channel")
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.type.value == 6:
            print('ites a delete')
            with open('/tmp/discordbot/management/delete_pinned.json', 'r') as f:
                channels = json.load(f)
                print(channels)
                for channel in channels:
                    if channel == ctx.channel.id:
                        await ctx.delete()

def setup(bot):
    bot.add_cog(Base(bot))