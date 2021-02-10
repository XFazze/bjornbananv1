import discord
import json
from discord.ext import commands, tasks
from discord.utils import get


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.noelcleanse.start()
    
    @commands.command(pass_context=True)
    async def newmembers(self, ctx):
        guild = ctx.guild
        for member in guild.members:
            if len(member.roles) == 1:
                message = "user: "+member.name
                await ctx.send(message)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def prime(self, ctx):
        guild = ctx.guild
        for member in ctx.message.mentions:
            
            role = get(guild.roles, id=802300233103048704)
            await member.add_roles(role)
            
            role = get(guild.roles, id=802305915491319838)
            await member.remove_roles(role)
        
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def noelbotadd(self, ctx):
        with open('/home/pi/discordbot/management/noelbot.json', 'r+') as f:
            noelbot = json.load(f)
            c_id = ctx.channel.id
            if c_id in noelbot:
                await ctx.send("This channel is already added to noelbot")
                print("tried to add noelbot but alreaddy added added")
            else:
                noelbot.append(c_id)
                await ctx.send("Added channel to noelbot")
                print("enabled noelbot")
                with open('/home/pi/discordbot/management/noelbot.json', 'w') as file:
                    json.dump(noelbot, file, indent=4)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def noelbotremove(self, ctx):
        with open('/home/pi/discordbot/management/noelbot.json', 'r+') as f:
            noelbot = json.load(f)
            c_id = ctx.channel.id
            if c_id in noelbot:
                noelbot.remove(c_id)
                await ctx.send("removed channel from noelbot")
                print("disabled noelbot")
                with open('/home/pi/discordbot/management/noelbot.json', 'w') as file:
                    json.dump(noelbot, file, indent=4)
            else:
                await ctx.send("This channel isnta a noelbot channel")
                print("tried to remove noelbot but wasnt added")
                
           

    @tasks.loop(seconds=10)
    async def noelcleanse(self):
        with open('/home/pi/discordbot/management/noelbot.json', 'r') as f:
            noelbot = json.load(f)
            for channel in noelbot:
                channel = self.bot.get_channel(channel)
                messages = await channel.history(limit=100).flatten()
                await channel.delete_messages(messages)
    
    @noelcleanse.before_loop
    async def before_noelcleanse(self):
        print('noelbot enabled')
        await self.bot.wait_until_ready()

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def rolebotadd(self, ctx):
        with open('/home/pi/discordbot/management/rolelog.json', 'r+') as f:
            rolelog = json.load(f)
            c_id = ctx.channel.id
            g_id = str(ctx.guild.id)
            if c_id in rolelog.values():
                await ctx.send("This channel is already added to rolelog")
                print("tried to add rolelog but alreaddy added added")
            else:
                rolelog[g_id] = c_id
                await ctx.send("Added channel to rolelog")
                print("enabled rolelog for server", ctx.guild)
                with open('/home/pi/discordbot/management/rolelog.json', 'w') as file:
                    json.dump(rolelog, file, indent=4)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def rolebotremove(self, ctx):
        with open('/home/pi/discordbot/management/rolelog.json', 'r+') as f:
            rolelog = json.load(f)
            c_id = ctx.channel.id
            g_id = str(ctx.guild.id)
            if c_id in rolelog.values():
                del rolelog[g_id]
                await ctx.send("removed channel to rolelog")
                print("disabled rolelog for server", ctx.guild)
                with open('/home/pi/discordbot/management/rolelog.json', 'w') as file:
                    json.dump(rolelog, file, indent=4)
            else:
                await ctx.send("This channel isnta a rolelog channel")
                print("tried to remove rolelog but wasnt added")
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles == after.roles:
            return
        else:
            with open('/home/pi/discordbot/management/rolelog.json', 'r') as f:
                rolelog = json.load(f)
                guild_id = str(before.guild.id)
                if guild_id not in rolelog.keys():
                    return
                channel_id = rolelog[guild_id]
                channel = self.bot.get_channel(channel_id)
                if len(before.roles) > len(after.roles):
                    role = list(set(before.roles)-set(after.roles))[0]
                    message = "User: "+ str(before) +"\nRole removed: " +role.name
                    await channel.send(message)
                else:
                    role = list(set(after.roles)-set(before.roles))[0]
                    if role.id == 802300001875001455:
                        message = "@everyopne User: "+ str(before) +"\nRole added: " +role.name
                    else:
                        message = "User: "+ str(before) +"\nRole added: " +role.name
                    await channel.send(message)
        

       

def setup(bot):
    bot.add_cog(Base(bot))