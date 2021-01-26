import discord
import time
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print(before, "\n", after)
        action = "admin abuse"
        if before.self_mute != after.self_mute:
            if before.self_mute:
                action = "unselfmute"
            elif after.self_mute:
                action = "selfmute"

        elif before.self_deaf != after.self_deaf:
            if before.self_deaf:
                action = "unselfdeaf"
            elif after.self_deaf:
                action = "selfdeaf"

        elif before.self_stream != after.self_stream:
            if before.self_stream:
                action = "unselfstream"
            elif after.self_stream:
                action = "selfstream"

        elif not before.channel:
            action = "connect " + str(after.channel)

        elif not after.channel:
            action = "disconnect " + str(before.channel)
        
        elif after.channel !=  before.channel:
            action = "move "+ str(before.channel) +" TO "+ str(after.channel)
        
        
        with open('/home/pi/discordbot/vc_logs.txt', 'a') as f:
            print(str(member)+" "+action)
            f.write(str(member)+" "+action + "\n")


def setup(bot):
    bot.add_cog(Base(bot))
