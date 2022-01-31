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
            if ctx.author.id == 243022798543519745:
                await ctx.reply(f'{num}/2100, WINS: {(2100-num)/10}  LOSSES: {(2100-num)/5}')
            else:
                await ctx.reply(f'{num}/16500, WINS: {(16500-num)/10}  LOSSES: {(16500-num)/5}')
            await ctx.delete()





def setup(bot):
    bot.add_cog(fabianLOL(bot))
