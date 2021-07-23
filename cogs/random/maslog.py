import discord
import time
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content[0:3] == ",,," and message.author.id == 243022798543519745:
            with open('/tmp/discordbot/maslog.txt', 'a') as f:
                f.write(str(time.time()) + " "+ message.content[3:]+"\n")
            await message.delete()

def setup(bot):
    bot.add_cog(Base(bot))