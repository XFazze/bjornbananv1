import discord
from discord.utils import get
from pymongo import MongoClient
from discord.ext import commands


class Bjornbanansetprefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#FIXME Does it work? 
# Björnbanan set prefix
    @commands.Cog.listener()
    @commands.has_permissions(manage_guild=True)
    async def on_message(self, message):
        msg = message.content
        if msg[0:19] != "bjornbanansetprefix":
            return
        if len(msg.split(' ')) != 2:
            embed = discord.Embed(
                title="Prove a valid prefix. bjornbanansetprefix [prefix]", color=0xFD3333)
            await message.channel.send(embed=embed)
            return

        prefix = msg.split(' ')[1]

        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": message.guild.id}
        config = collection.find_one(myquery)["config"]

        config["prefix"] = prefix
        newvalue = {"$set": {"config": config}}
        collection.update_one(myquery, newvalue)
        embed = discord.Embed(
            title="Successfully changed the prefix to " + prefix, color=0x00FF42)
        await message.channel.send(embed=embed)




def setup(bot):
    bot.add_cog(Bjornbanansetprefix(bot))
