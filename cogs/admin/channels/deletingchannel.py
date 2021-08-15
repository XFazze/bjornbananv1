import discord
import json
from discord.ext import commands, tasks
from discord.utils import get

# channels which get cleansed every 10 seoncds
class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cleanse.start()

    @commands.command(pass_context=True, aliases=['ed'])
    @commands.has_permissions(manage_messages=True)
    async def enabledelete(self, ctx):
        with open('/tmp/discordbot/management/deletingchannel.json', 'r+') as f:
            deletingchannel = json.load(f)
            c_id = ctx.channel.id
            if c_id in deletingchannel:
                await ctx.send("This channel is already added to deletingchannel")
            else:
                deletingchannel.append(c_id)
                await ctx.send("Added channel to deletingchannel")
                with open('/tmp/discordbot/management/deletingchannel.json', 'w') as file:
                    json.dump(deletingchannel, file, indent=4)

    @commands.command(pass_context=True, aliases=['dd'])
    @commands.has_permissions(manage_messages=True)
    async def disabledelete(self, ctx):
        with open('/tmp/discordbot/management/deletingchannel.json', 'r+') as f:
            deletingchannel = json.load(f)
            c_id = ctx.channel.id
            if c_id in deletingchannel:
                deletingchannel.remove(c_id)
                await ctx.send("removed channel from deletingchannel")
                with open('/tmp/discordbot/management/deletingchannel.json', 'w') as file:
                    json.dump(deletingchannel, file, indent=4)
            else:
                await ctx.send("This channel isnta a deletingchannel channel")

    @tasks.loop(seconds=10)
    async def cleanse(self):
        with open('/tmp/discordbot/management/deletingchannel.json', 'r') as f:
            deletingchannel = json.load(f)
            if deletingchannel:
                for channel in deletingchannel:
                    channel = self.deletingchannel.get_channel(channel)
                    messages = await channel.history(limit=100).flatten()
                    await channel.delete_messages(messages)

    @cleanse.before_loop
    async def before_cleanse(self):
        print('deletingchannel enabled')
        await self.cleanse.wait_until_ready()

def setup(bot):
    bot.add_cog(Base(bot))