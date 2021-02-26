import discord
import json
import random
from discord.ext import commands
from discord.utils import get


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ticket(self, ctx):
        f = json.load(open("servers.json", "r"))
        if str(ctx.message.guild.id) not in f["ticket"]:
            await ctx.send("COMMAND NOT ALLOWED IN YOUR HOME")
            return
        guild = ctx.guild
        tickets = True
        
        for cat in guild.categories:
            if cat.name == "tickets":
                tickets = False
                category = cat
        
        if tickets:
            category = await guild.create_category("tickets")
            await category.set_permissions(guild.default_role, read_messages=False)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            role = get(guild.roles, id=802299956299169845)
            await category.set_permissions(role, overwrite=overwrite)
        
        name = str(random.randint(111111,999999))+"_"+str(ctx.author)
        channel = await guild.create_text_channel(name=name, category=category)
        await channel.set_permissions(guild.default_role, read_messages=False)
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = True
        await channel.set_permissions(ctx.author, overwrite=overwrite)
        admin = get(guild.roles, id=802299956299169845)
        await channel.set_permissions(admin, overwrite=overwrite)
        message = await channel.send("Here you can contact the admins if you have a report or a proposal. When finished react with the :lock: to this message.")
        await message.add_reaction("🔒")
        

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        guild = self.bot.get_guild(payload.guild_id)
        if message.author == guild.get_member(self.bot.user.id) and payload.member != guild.get_member(self.bot.user.id) and channel.category_id == 808279224485806110:
            bigmessage = []
            file = "/home/pi/discordbot/tickets/"+channel.name+".txt"
            with open(file, "w+") as f:
                newhistory = []
                async for message in channel.history(limit=20000):
                    newhistory.insert(0, message)
                for message in newhistory:
                    f.write(message.author.name +":"+ message.content + "\n")
            await channel.delete()
            for member in channel.members:
                await member.send(file=discord.File(file))
def setup(bot):
    bot.add_cog(Base(bot))