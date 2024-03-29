import discord
#from ..admin.managecommands import perms
from discord.ext import commands


class embedsender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def sendembed(self, ctx, color = None, title=None, fields=''):
        
        if not color:
            color = 0x000000
        if not title:
            title = 'v'
            
        color = int(color, 16)
        if color >= 16777215:
            await ctx.reply(embed=discord.Embed(title="Cant convert color to hex. Provide hex code as '000000' or '0x000000'.", color=0xFD3333))
            return

        embed = discord.Embed(title=title, color=color)
        try:
            for field in fields.split(',,,'):
                name = field.split(',,')[0]
                description = field.split(',,')[1]
                embed.add_field(name=name, value=description, inline=False)


            await ctx.send(embed=embed) 
            await ctx.message.delete()
        except:
            title = 'Error. example: ,sendembed 111111 \"a a \"  \"pool,, papa,,,new field,,values\"'
            await ctx.reply(embed=discord.Embed(title=title, color=0xFD3333))

        
    



def setup(bot):
    bot.add_cog(embedsender(bot))