import discord
import time
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        action = "admin abuse"
        if before.self_mute != after.self_mute:
            channnel_id = before.channel.id
            if before.self_mute:
                action = "unselfmute"
            elif after.self_mute:
                action = "selfmute"

        elif before.self_deaf != after.self_deaf:
            channnel_id = before.channel.id
            if before.self_deaf:
                action = "unselfdeaf"
            elif after.self_deaf:
                action = "selfdeaf"

        elif before.self_stream != after.self_stream:
            channnel_id = before.channel.id
            if before.self_stream:
                action = "unselfstream"
            elif after.self_stream:
                action = "selfstream"

        elif not before.channel:
            channnel_id = after.channel.id
            action = "connect"

        elif not after.channel:
            channnel_id = before.channel.id
            action = "disconnect" 
        
        elif after.channel !=  before.channel:
            channnel_id = [after.channel.id, before.channel.id]
            action = "move"
        
        
        with open('/home/pi/discordbot/vc_logs.txt', 'a') as f:
            f.write(str(time.time())+" "+ action+" "+ str(channnel_id) + " "+str(member)+ "\n")

    
    @commands.Cog.listener()
    async def on_message(self, message):
        member = await message.guild.fetch_member(message.author.id)
        with open('/home/pi/discordbot/tc_logs.txt', 'a') as f:
            f.write(str(time.time()) + " send "   + str(message.guild.id)+ " "+ str(message.channel.id)+ " "+str(message.id) +" "+ str(member) + " "+ "\n")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        with open('/home/pi/discordbot/tc_logs.txt', 'a') as f:
            f.write(str(time.time()) + " delete " + str(payload.guild_id) +" "+ str(payload.channel_id) +" "+ str(payload.message_id) + " "+ "\n")
            
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        with open('/home/pi/discordbot/tc_logs.txt', 'a') as f:
            f.write(str(time.time()) + " edit " + str(payload.data["guild_id"]) + " " + str(payload.data["channel_id"]) +" "+ str(payload.data["id"]) + " "+ str(payload.data["author"]["username"])+ "#"+str(payload.data["author"]["discriminator"]) + "\n")
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        with open('/home/pi/discordbot/tc_logs.txt', 'a') as f:
            f.write(str(time.time()) + " reactadd " + str(payload.guild_id) +" "+ str(payload.channel_id) +" "+ str(payload.message_id) + " " + str(payload.member.name) +"#"+ str(payload.member.discriminator) + " " + str(payload.emoji.name) +"\n")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        print(payload)
        guild = self.bot.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        with open('/home/pi/discordbot/tc_logs.txt', 'a') as f:
            f.write(str(time.time()) + " reactremove " + str(payload.guild_id) +" "+ str(payload.channel_id) +" "+ str(payload.message_id) + " " + str(member) + " " + str(payload.emoji.name) +"\n")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):        
        with open('/home/pi/discordbot/tc_logs.txt', 'a') as f:
            f.write(str(time.time()) + " typing "  +str(channel.guild.id) + " "+ str(channel.id) +" " +str(user)+"\n")


# channel create(private), channel delete, channel update
# role create, role delete, role update
# guild join, guild remove, guild update
# guild emoji update
# ban unban
# invite create remove

def setup(bot):
    bot.add_cog(Base(bot))
