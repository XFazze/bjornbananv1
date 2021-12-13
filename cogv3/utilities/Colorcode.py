from ..admin.managecommands import perms
from discord.ext import commands
import re


class Colorcode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# Colorcode
    @commands.command(pass_context=True, aliases=['cc'])
    @commands.check(perms)
    async def colorcode(self, ctx):
        await ctx.message.delete()
        for role in ctx.message.author.roles:
            if str(role)[0] == ";":
                if len(str(ctx.message.content).split(" ")) > 1:
                    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', "#"+str(ctx.message.content).split(" ")[1]):
                        await role.edit(color=int(("0x"+str(ctx.message.content).split(" ")[1]), 16), reason="Testing")
                        await ctx.reply("Successfully changed Color of your role")
                        return
                    else:
                        await ctx.reply("Colorcode is invalid format:gcolor ffffff")
                        return
                else:
                    await ctx.reply("You need to provide a color code like this:gcolor ffffff")
                    return
        await ctx.reply("You dont have a role. \nSo I will create a role for you:")
        role_name = ";"+str(ctx.message.author)[0:-5]
        await ctx.reply(role_name)
        role = await ctx.guild.create_role(name=role_name)
        await ctx.message.author.add_roles(role)
        await ctx.reply("I have also given you the roles you're welcume")
    


def setup(bot):
    bot.add_cog(Colorcode(bot))