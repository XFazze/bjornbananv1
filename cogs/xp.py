import discord
import time
import random
from discord.ext import tasks, commands


    




class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_xp.start()

    @tasks.loop(seconds=15)
    async def all_xp(self):
        print("tc")
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
            print(tc_formated)


def setup(bot):
    bot.add_cog(Base(bot))
