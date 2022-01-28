from ..admin.managecommands import perms
from discord.ext import commands, tasks
from discord.utils import get


class fabianLOL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Role log
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.channel.id == 936101882387103765 and ctx.author != self.bot.user:
            try:
                num = int(ctx.content)
            except:
                return
            if ctx.author.id == 212483159659380739:
                await ctx.reply(f'{num}/3600, WINS: {(3600-num)/10}  LOSSES: {(3600-num)/5}')
            else:
                await ctx.reply(f'{num}/16500, WINS: {(16500-num)/10}  LOSSES: {(16500-num)/5}')
            await ctx.delete()





def setup(bot):
    bot.add_cog(fabianLOL(bot))
