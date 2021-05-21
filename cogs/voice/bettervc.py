import discord
import json
from discord.ext import commands, tasks
from discord.utils import get



class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidechannels.start()

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def eb(self, ctx):
        with open('/home/pi/discordbot/management/bettervc.json', 'r+') as f:
            bettervc = json.load(f)
            if str(ctx.author.voice.channel.guild.id) in bettervc.keys():
                await ctx.send("category already decided, remove if changing")
            else:
                await ctx.send("adding category to bettervc")
                bettervc[str(ctx.author.voice.channel.guild.id)] = ctx.author.voice.channel.category_id
                with open('/home/pi/discordbot/management/bettervc.json', 'w') as file:
                    json.dump(bettervc, file, indent=4)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def db(self, ctx):
        with open('/home/pi/discordbot/management/bettervc.json', 'r+') as f:
            bettervc = json.load(f)
            if str(ctx.author.voice.channel.guild.id) in bettervc.keys():
                await ctx.send("removing category from bettervc")
                del bettervc[str(ctx.author.voice.channel.guild.id)]
                with open('/home/pi/discordbot/management/bettervc.json', 'w') as file:
                    json.dump(bettervc, file, indent=4)
            else:
                await ctx.send("category isn't in bettervc")
    
    @tasks.loop(seconds=10)
    async def hidechannels(self):
        with open('/home/pi/discordbot/management/bettervc.json', 'r+') as f:
            bettervc = json.load(f)
            for guild_id in bettervc.keys():
                guild = self.bot.get_guild(int(guild_id))
                category = get(guild.categories, id=bettervc[str(guild_id)])
                empty_channels = []
                for channel in category.channels:
                    if len(channel.members) == 0:
                        empty_channels.append(channel)
                empty_channels.pop(0)
                for hiding_channel in empty_channels:
                    await hiding_channel.set_permissions(guild.default_role, read_messages=False)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        with open('/home/pi/discordbot/management/bettervc.json', 'r+') as f:
            bettervc = json.load(f)
            try:
                if after.channel.category_id in bettervc.values():
                    if len(after.channel.members) == 1:
                        for guild_id, category_id in bettervc.items():
                            if after.channel.category_id == category_id:
                                guild = self.bot.get_guild(int(guild_id))
                                category = get(guild.categories, id=bettervc[str(guild_id)])
                                for empty_channel in category.channels:
                                    if len(empty_channel.members) == 0:
                                        await empty_channel.set_permissions(guild.default_role, read_messages=None)
                                        break
            except:
                return

                    
    
    @hidechannels.before_loop
    async def before_hidechannels(self):
        print('bettervc enabled')
        await self.bot.wait_until_ready()

    

def setup(bot):
    bot.add_cog(Base(bot))