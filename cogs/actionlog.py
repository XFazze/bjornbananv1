import discord
import time
import math
import os
from discord.ext import commands

class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        action = "admin abuse"
        
        if before.self_deaf != after.self_deaf:
            channel_id = before.channel.id
            if before.self_deaf:
                action = "unselfdeaf"
            elif after.self_deaf:
                action = "selfdeaf"
                
        elif before.self_mute != after.self_mute:
            channel_id = before.channel.id
            if before.self_mute:
                action = "unselfmute"
            elif after.self_mute:
                action = "selfmute"

       

        elif before.self_stream != after.self_stream:
            channel_id = before.channel.id
            if before.self_stream:
                action = "unselfstream"
            elif after.self_stream:
                action = "selfstream"

        elif not before.channel:
            channel_id = after.channel.id
            action = "connect"

        elif not after.channel:
            channel_id = before.channel.id
            action = "disconnect" 
        
        elif after.channel !=  before.channel:
            channel_id = [after.channel.id, before.channel.id]
            action = "move"

        if action == "admin abuse":
            return
            
        filename = '/home/pi/discordbot/vc_logs/'+str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time())+" "+ action+" "+ str(channel_id) + " "+str(member)+ "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time())+" "+ action+" "+ str(channel_id) + " "+str(member)+ "\n")

    
    @commands.Cog.listener()
    async def on_message(self, message):
        member = await message.guild.fetch_member(message.author.id)
        filename = '/home/pi/discordbot/tc_logs/'+str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " send "   + str(message.guild.id)+ " "+ str(message.channel.id)+ " "+str(message.id) +" "+ str(member) + " "+ "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " send "   + str(message.guild.id)+ " "+ str(message.channel.id)+ " "+str(message.id) +" "+ str(member) + " "+ "\n")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        filename = '/home/pi/discordbot/tc_logs/'+str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " delete " + str(payload.guild_id) +" "+ str(payload.channel_id) +" "+ str(payload.message_id) + " "+ "\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " delete " + str(payload.guild_id) +" "+ str(payload.channel_id) +" "+ str(payload.message_id) + " "+ "\n")
            
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        filename = '/home/pi/discordbot/tc_logs/'+str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " edit " + str(payload.data["guild_id"]) + " " + str(payload.data["channel_id"]) +" "+ str(payload.data["id"]) + " "+ str(payload.data["author"]["username"]) + "#" + str(payload.data["author"]["discriminator"]) +  "\n")
        except:
            try:
                with open(filename, 'w') as f:
                    f.write(str(time.time()) + " edit " + str(payload.data["guild_id"]) + " " + str(payload.data["channel_id"]) +" "+ str(payload.data["id"]) + " "+ str(payload.data["author"]["username"]) + "#" + str(payload.data["author"]["discriminator"]) +  "\n")
            except:
                print("the strange thing happeneded in actionlog")
                
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        filename = '/home/pi/discordbot/tc_logs/'+str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " reactadd " + str(payload.guild_id) +" "+ str(payload.channel_id) +" "+ str(payload.message_id) + " " + str(payload.member.name) +"#"+ str(payload.member.discriminator) + " " + str(payload.emoji.name) +"\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " reactadd " + str(payload.guild_id) +" "+ str(payload.channel_id) +" "+ str(payload.message_id) + " " + str(payload.member.name) +"#"+ str(payload.member.discriminator) + " " + str(payload.emoji.name) +"\n")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        filename = '/home/pi/discordbot/tc_logs/'+str(math.floor(time.time()/86400))+'.txt'
        try:
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " reactremove " + str(payload.guild_id) +" "+ str(payload.channel_id) +" "+ str(payload.message_id) + " " + str(member) + " " + str(payload.emoji.name) +"\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " reactremove " + str(payload.guild_id) +" "+ str(payload.channel_id) +" "+ str(payload.message_id) + " " + str(member) + " " + str(payload.emoji.name) +"\n")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):      
        filename = '/home/pi/discordbot/tc_logs/'+str(math.floor(time.time()/86400))+'.txt'
        try:  
            with open(filename, 'a') as f:
                f.write(str(time.time()) + " typing "  +str(channel.guild.id) + " "+ str(channel.id) +" " +str(user)+"\n")
        except:
            with open(filename, 'w') as f:
                f.write(str(time.time()) + " typing "  +str(channel.guild.id) + " "+ str(channel.id) +" " +str(user)+"\n")
            


# channel create(private), channel delete, channel update
# role create, role delete, role update
# guild join, guild remove, guild update
# guild emoji update
# ban unban
# invite create remove
    @commands.command(pass_context=True)
    async def vcstats(self, ctx):
        with open('/home/pi/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "vcstats" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return

        directory = os.fsencode('/home/pi/discordbot/vc_logs/')
        bigfileline=[]
        for file in os.listdir(directory):
            filename = '/home/pi/discordbot/vc_logs/'+os.fsdecode(file)
            with open(filename, 'r') as file:
                filelines = file.readlines()
                for line in filelines:
                    bigfileline.append(line)
        minutes={}
        for line in bigfileline:
            linelist = line.split(" ")
            if linelist[1] == "connect":
                line_num = bigfileline.index(line)
                for iline in bigfileline[line_num:]:
                    ilinelist = iline.split(" ")
                    if ilinelist[1] == "disconnect" and str(linelist[3])[:-1] == str(ilinelist[3])[:-1]:
                        trime = int(math.floor((float(ilinelist[0])/60 - float(linelist[0])/60)))
                        name = str(linelist[3])[:-1]
                        if name in minutes.keys():
                            minutes[name] = minutes[name]+trime
                        else:
                            minutes[name] = trime
                        break

        minutes =  dict(sorted(minutes.items(), key=lambda item: item[1]))
        mess = ""
        for item in minutes:
            mess = mess + str(minutes[item]) + "   :   "+str(item)+"\n"
        await ctx.send(mess)


    @commands.command(pass_context=True)
    async def tcstats(self, ctx):
        with open('/home/pi/discordbot/management/enable.json', 'r+') as f:
            enable = json.load(f)
            if "tcstats" in enable[str(ctx.guild.id)]:
                await ctx.send("Command not allowed in this server")
                return

        directory = os.fsencode('/home/pi/discordbot/tc_logs/')
        bigfileline=[]
        for file in os.listdir(directory):
            filename = '/home/pi/discordbot/tc_logs/'+os.fsdecode(file)
            with open(filename, 'r') as file:
                filelines = file.readlines()
                for line in filelines:
                    bigfileline.append(line)

        messages = {}

        for line in bigfileline:
            linelist = line.split(" ")
            if linelist[1] == "send":
                name = str(linelist[5])[:-1]
                if name in messages.keys():
                    messages[name] = messages[name]+1
                else:
                    messages[name] = 1
        
        
        messages =  dict(sorted(messages.items(), key=lambda item: item[1]))
        mess = ""
        for item in messages:
            mess = mess +str(messages[item]) + "   :   " +  str(item) + "\n"
        await ctx.send(mess)

def setup(bot):
    bot.add_cog(Base(bot))
