import discord
import json
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
from discord.utils import get


class Better_vc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cleanse.start()

    @tasks.loop(seconds=10)
    async def cleanse(self):
        collection = MongoClient('localhost', 27017).maindb.guilds
        guilds = collection.find({})
        for guild in guilds:
            guild_object = self.bot.get_guild(guild["id"])
            if len(guild["config"]["bettervc"]) != 0:
                for category in guild["config"]["bettervc"]:
                    category_object = get(self.bot.get_all_channels(), id=category)
                    empty_channels = []
                    for channel in category_object.channels:
                        if len(channel.members) == 0:
                            empty_channels.append(channel)
                    empty_channels.pop(0)
                    for hiding_channel in empty_channels:
                        await hiding_channel.set_permissions(guild_object.default_role, read_messages=False)

    @cleanse.before_loop
    async def before_cleanse(self):
        print("Bettervc enabled")
        await self.bot.wait_until_ready()
       


def setup(bot):
    bot.add_cog(Better_vc(bot))
