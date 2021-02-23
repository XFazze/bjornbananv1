import discord
import time
import random
import math
from discord.ext import tasks, commands


    




class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_xp.start()

    @tasks.loop(seconds=15)
    async def all_xp(self):
        with open('/home/pi/discordbot/tc_logs.txt', 'r') as tc_logs:
            tc_log_content = tc_logs.readlines()
            tc_formated = {}
            lasttime = time.time()-15
            for line in tc_log_content:
                tmp = line[:-2].split(" ")
                if float(tmp[0]) > lasttime:
                    if tmp[1] == "send":
                        try:
                            tc_formated[tmp[5]] += 1
                            if tc_formated[tmp[5]] > 3 and random.randint(0,1) >0.8:
                                tc_formated[tmp[5]] = round(tc_formated[tmp[5]]/2)
                        except:
                            tc_formated[tmp[5]] = 1
    @all_xp.before_loop
    async def before_all_xp(self):
        print('all xp enabled')
        await self.bot.wait_until_ready()

    @commands.command(pass_context=True)
    async def vcstats(self, ctx):
        with open('/home/pi/discordbot/vc_logs.txt', 'r') as file:
            filelines = file.readlines()
        minutes={}
        for line in filelines:
            linelist = line.split(" ")
            if linelist[1] == "connect":
                line_num = filelines.index(line)
                for iline in filelines[line_num:]:
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
        with open('/home/pi/discordbot/tc_logs.txt', 'r') as file:
            filelines = file.readlines()
        messages = {}

        for line in filelines:
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
             mess = mess +str(messages[item]),"   :   ", item
        await ctx.send(mess)


def setup(bot):
    bot.add_cog(Base(bot))
