import discord
from discord.ext import commands
from discord.ext.commands import bot
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["discordbot"]           # Database
dbg = db["guilds"]                  # Collection



class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, aliases=['latency'])
    async def ping(self, ctx):
        if dbg.find({"_id":ctx.guild.id}).count() > 0:
            print("This guild is registered")
        else:
            dbg.insert_one({"_id" : ctx.guild.id,
                            "name" : ctx.guild.name})
            print(f"Registered {ctx.guild.id}")
        

        
        
        for x in dbg.find():
            print(x)
        
        
        
        
        #await ctx.message.delete()
        embed = discord.Embed(colour=0xFFFFFF)
        embed.add_field(name="Latency", value='{0}ms'.format(round(self.bot.latency*1000, 1)))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Ping(bot))