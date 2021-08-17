import discord
import json
from discord.ext import commands
from discord.utils import get


class Join_roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    # Reaction roles

    @commands.command(pass_context=True, aliases=['jra', 'jradd'])
    @commands.has_permissions(manage_roles=True)
    async def joinroleadd(self, ctx):
        try:
            role_id = int(str(ctx.message.content).split(" ")[1][3:-1])
        except:
            await ctx.send("you forgot the role")
            return

        guild_id = ctx.message.guild.id
        with open('/tmp/discordbot/management/joinrole.json', 'r+') as f:
            joinrole = json.load(f)
            if str(guild_id) in joinrole.keys():
                if role_id in joinrole[str(guild_id)]:
                    await ctx.send("This channel is already added to joinrole")
                else:
                    joinrole[str(guild_id)].append(role_id)
                    await ctx.send("Added channel to joinrole")
                    with open('/tmp/discordbot/management/joinrole.json', 'w') as file:
                        json.dump(joinrole, file, indent=4)
            else:
                joinrole[int(guild_id)] = [role_id]
                await ctx.send("Added channel to joinrole")
                with open('/tmp/discordbot/management/joinrole.json', 'w') as file:
                    json.dump(joinrole, file, indent=4)

    @commands.command(pass_context=True, aliases=['jrr', 'jrremove'])
    @commands.has_permissions(manage_roles=True)
    async def joinroleremove(self, ctx):
        try:
            role_id = int(str(ctx.message.content).split(" ")[1][3:-1])
        except:
            await ctx.send("you forgot the role")
            return

        guild_id = ctx.message.guild.id
        with open('/tmp/discordbot/management/joinrole.json', 'r+') as f:
            joinrole = json.load(f)
            if str(guild_id) in joinrole.keys():
                print("exist")
                if role_id in joinrole[str(guild_id)]:
                    if len(joinrole[str(guild_id)]) > 1:
                        joinrole[str(guild_id)].remove(role_id)
                        with open('/tmp/discordbot/management/joinrole.json', 'w') as file:
                            json.dump(joinrole, file, indent=4)
                    else:
                        del joinrole[str(guild_id)]
                        with open('/tmp/discordbot/management/joinrole.json', 'w') as file:
                            json.dump(joinrole, file, indent=4)
                    await ctx.send("This role is removed")
                else:
                    await ctx.send("Channel not added")
            else:
                await ctx.send("Channel not added")

    @commands.command(pass_context=True, aliases=['jrl', 'jrlist'])
    async def joinrolelist(self, ctx):
        guild = ctx.guild
        embed=discord.Embed(title="Join roles", color=0xFFF4E6)
        with open('/tmp/discordbot/management/joinrole.json', 'r+') as f:
            joinrole = json.load(f)
            if str(guild.id) in joinrole.keys():
                for role_id in joinrole[str(guild.id)]:
                    role = get(guild.roles, id=role_id)
                    embed.add_field(name=role.name, value="\u200b", inline=False)
            else:
                embed.add_field(name="Mission failed", value="There are no join roles on this server", inline=False)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        with open('/tmp/discordbot/management/joinrole.json', 'r+') as f:
            joinrole = json.load(f)
            if str(guild.id) in joinrole.keys():
                for role_id in joinrole[str(guild.id)]:
                    role = get(guild.roles, id=role_id)
                    await member.add_roles(role)


def setup(bot):
    bot.add_cog(Join_roles(bot))