import discord
import random
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content[0] != "d":
            return
        try:
            notd = message.content[1:].split(" ")
            rollamount = int(notd[0])
            notd.pop(0)
        except:
            print("didnt provide number")
            return
        outcome = random.randint(1, rollamount)
        result = outcome
        try:
            for operator in notd:
                if operator[0] == "+":
                    result = result+int(operator[1:])
                if operator[0] == "-":
                    result = result-int(operator[1:])
                if operator[0] == "/":
                    result = result/int(operator[1:])
                if operator[0] == "*":
                    result = result*int(operator[1:])
        except:
            await message.channel.send(f'You inputed wrong operators("+2","-3", "/2", "*5")')
        await message.channel.send(f"```d{rollamount}:{outcome} {' '.join(map(str,notd))}= {result}```")
        print("roll done")

    @commands.command(pass_context=True, aliases=['dndframer'])
    @commands.has_permissions(manage_channels=True)
    async def dndframe(self, ctx):
        try:
            name = ctx.message.content[11:].split(",")[0]
        except:
            print("invalid name")
            await ctx.send('format was wrong("gdndframer your name @person1 @person2")')
        guild = ctx.guild
        role = await guild.create_role(name=name)
        dm = ctx.message.author
        players = ctx.message.mentions
        await dm.add_roles(role)

        category = await guild.create_category(name)
        await category.set_permissions(guild.default_role, read_messages=False)
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = True
        await category.set_permissions(role, overwrite=overwrite)
        for player in players:
            await player.add_roles(role)
            print(type(player.display_name))
            channel_perm = await guild.create_text_channel(name=player.display_name+" dm", category=category)
            await channel_perm.set_permissions(role, read_messages=False)
            await channel_perm.set_permissions(dm, overwrite=overwrite)
            await channel_perm.set_permissions(player, overwrite=overwrite)

        channels = [name, "dice", "viktigt", "kartor", "stats", "initiative"]
        vc_channels = ["talk", "hjälp av dm"]
        dm_channels = ["dice-dm", "endast-dm", "hp-dm"]
        for channel in channels:
            await guild.create_text_channel(name=channel, category=category)
        for channel in vc_channels:
            await guild.create_voice_channel(name=channel, category=category)
        for channel in dm_channels:
            channel_perm = await guild.create_text_channel(name=channel, category=category)
            await channel_perm.set_permissions(role, read_messages=False)
            await channel_perm.set_permissions(dm, overwrite=overwrite)

        


def setup(bot):
    bot.add_cog(Base(bot))
