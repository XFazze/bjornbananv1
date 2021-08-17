import discord
import json
from discord.ext import commands


class Enable_disable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def disable(self,ctx):
        try:
            command = str(ctx.message.content).split(" ")[1]
        except:
            await ctx.send("Provide a command")
        if command in ["enable", "disable"]:
            await ctx.send("cant disable this command")
        for botcommand in  self.bot.commands:
            if command == str(botcommand):
                guild_id = ctx.guild.id
                with open('/tmp/discordbot/management/enable.json', 'r+') as f:
                    enable = json.load(f)
                    if str(guild_id) in enable.keys():
                        if command in enable[str(guild_id)]:
                            await ctx.send("This command is already disabled")
                        else:
                            enable[str(guild_id)].append(command)
                            await ctx.send("Disabled command")
                            with open('/tmp/discordbot/management/enable.json', 'w') as file:
                                json.dump(enable, file, indent=4)
                    else:
                        enable[int(guild_id)] = [command]
                        await ctx.send("Disabled command")
                        with open('/tmp/discordbot/management/enable.json', 'w') as file:
                            json.dump(enable, file, indent=4)
    
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def enable(self,ctx):
        try:
            command = str(ctx.message.content).split(" ")[1]
        except:
            await ctx.send("Provide a command")
        if command in ["enable", "disable"]:
            await ctx.send("cant disable this command")
        for botcommand in  self.bot.commands:
            if command == str(botcommand):
                guild_id = ctx.guild.id
                with open('/tmp/discordbot/management/enable.json', 'r+') as f:
                    enable = json.load(f)
                    if str(guild_id) in enable.keys():
                        print("exist")
                        if command in enable[str(guild_id)]:
                            if len(enable[str(guild_id)]) > 1:
                                enable[str(guild_id)].remove(command)
                                with open('/tmp/discordbot/management/enable.json', 'w') as file:
                                    json.dump(enable, file, indent=4)
                            else:
                                del enable[str(guild_id)]
                                with open('/tmp/discordbot/management/enable.json', 'w') as file:
                                    json.dump(enable, file, indent=4)
                            await ctx.send("This command is enabled")
                            return
                        else:
                            await ctx.send("Command already allowed")
                            return
                    else:
                        await ctx.send("Command already allowed")
                        return
        await ctx.send("Command does not exist")
        
            




def setup(bot):
    bot.add_cog(Enable_disable(bot))