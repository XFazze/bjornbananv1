import discord
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def text_xp():
        while True:
            print("fycj ea")
            await asyncio.sleep(5)

    @commands.Cog.listener()
    async def on_ready(self):
        print(self, type(self))

def setup(bot):
    bot.add_cog(Base(bot))