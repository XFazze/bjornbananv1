import discord
from discord.ext import commands
from discord.utils import get


class Base(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    # Reaction roles

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def rear(self, ctx):
        if checkenable("vcstats", ctx.guild.id):
            await ctx.send("command not allowed")
            return
        try:
            role_id = int(str(ctx.message.content).split(" ")[1][3:-1])
        except:
            print("forgot variable role")
            await ctx.send("you forgot the role variable, format: grear @role emoji text. OBS spaces")
            return
        try:
            emoji = str(ctx.message.content).split(" ")[2]
        except:
            print("forgot variable emoji")
            await ctx.send("you forgot the amoji variable, format: grear @role emoji text. OBS spaces")
            return
        try:
            text = str(ctx.message.content).split(" ")[3:]
        except:
            print("forgot variable text")
            await ctx.send("you forgot the text variable, format: grear @role emoji text. OBS spaces")
            return
        highest_role = ctx.message.author.roles[-1]
        role = get(ctx.guild.roles, id=role_id)
        for roles in ctx.guild.roles:
            if role == roles:
                print("He's allowed")
                break
            elif highest_role == roles:
                print("he's not allowed")
                return
        phrase = ""
        for word in text:
            phrase = phrase+" "+word
        message = "Role: "+str(role) + " |" + phrase

        bot_message = await ctx.send(message)
        await bot_message.add_reaction(emoji)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(
            message.reactions, emoji=payload.emoji.name)
        guild = self.bot.get_guild(payload.guild_id)
        if message.author == guild.get_member(self.bot.user.id) and "Role:" == str(message.content)[0:5] and payload.member != guild.get_member(self.bot.user.id):
            role = str(message.content)[6:].split(" |")[0]
            role = discord.utils.get(guild.roles, name=role)
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(
            message.reactions, emoji=payload.emoji.name)
        guild = self.bot.get_guild(payload.guild_id)
        if message.author == guild.get_member(self.bot.user.id) and "Role:" == str(message.content)[0:5]:
            role = str(message.content)[6:].split(" |")[0]
            role = discord.utils.get(guild.roles, name=role)
            member = await guild.fetch_member(payload.user_id)
            await member.remove_roles(role)

    @commands.command(pass_context=True)
    async def reac(self, ctx):
        with open('/home/pi/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "rear" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return
        await ctx.message.delete()
        channel = ctx.message.channel
        messages = await channel.history(limit=200).flatten()
        print("found messages")
        tosend = []
        for message in messages:
            if message.content[0:6] == "Role: " and message.author == ctx.guild.get_member(self.bot.user.id) and message.reactions != []:
                tosend.insert(0, {"content": message.content,
                               "reaction": message.reactions[0]})
                await message.delete()
        print("done withe delete")
        for sending in tosend:
            msg = await ctx.send(sending["content"])
            await msg.add_reaction(sending["reaction"])
        print("sent again")


def setup(bot):
    bot.add_cog(Base(bot))
