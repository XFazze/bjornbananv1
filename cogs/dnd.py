import discord
import random
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg=message.content
        if msg[0] != "d":
            return
        try:
            print(msg)
            for sym in msg[1:]:
                print(sym, type(sym))
                if sym in "+-*/":
                    print("success")
                else:
                    p = int(sym)
            new = []
            temp = ""
            for symbol in msg:
                try:
                    x = int(symbol)
                    temp = temp+symbol
                except:
                    new.append(temp)
                    new.append(symbol)
                    temp = ""
            new.append(temp)
            dice = int(new[2])
            new[0] = random.randint(1, dice)
            new[1:]=new[3:]
            x = 1
            value = []
            operator=[]
            for i in new:
                x = x*-1
                if x < 0:
                    value.append(i)
                else:
                    operator.append(i)


            result = value[0]
            for op in operator:
                x = operator.index(op)
                if op == "+":
                    result = result+int(value[x+1])
                if op == "-":
                    result = result-int(value[x+1])
                if op == "/":
                    result = result/int(value[x+1])
                if op == "*":
                    result = result*int(value[x+1])
            print(f"success  {value[0]} {result}")
            await message.channel.send(f"```d{dice}:{value[0]} = {result}```")
        except:
            print("not a dice")

    @commands.command(pass_context=True, aliases=['dndframer'])
    @commands.has_permissions(manage_channels=True)
    async def dndframe(self, ctx):
        f = json.load(open("servers.json", "r"))
        if str(ctx.message.guild.id) not in f["dndframe"]:
            print("not allowed on server")
            await ctx.send("COMMAND NOT ALLOWED IN YOUR HOME")
            return
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
