import discord
import random
from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.content[0] != "d":
            return
        try:
            notd = message.content[1:].split(" ")
            rollamount = int(notd[0])
            notd.pop(0)
        except:
            print("didnt provide number")
            return
        outcome = random.randint(1,rollamount)
        result = outcome
        try:
            for operator in notd:
                if operator[0] == "+":
                    result = result+int(operator[1:])
                if operator[0] == "-":
                    result = result-int(operator[1:])
                if operator[0] == "/":
                    result = result/int(operator[1:])
                if operator[0] == "*":
                    result = result*int(operator[1:])
        except:
            await message.channel.send(f'You inputed wrong operators("+2","-3", "/2", "*5")')
        await message.channel.send(f"```d{rollamount}:{outcome} {' '.join(map(str,notd))}= {result}```")
        print("roll done")
    
    @commands.command(pass_context=True, aliases=['dndframer', '.dndframe'])
    async def dndframe(self,ctx):
        print("hey")
        

def setup(bot):
    bot.add_cog(Base(bot))