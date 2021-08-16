import random
import discord
import json
from discord import emoji
from discord.ext import commands



class Bomb_reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['boom', 'bomb', 'reactions'])
    async def bomb_reactions(self, ctx, *id):
        emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '☺', '😊', '😇', '🙂', '🙃',
                    '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐',
                    '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹',  '😣',
                    '😖', '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬', '🤯', '😳', '🥵', '🥶', '😱',
                    '😨', '😰', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯',
                    '😦', '😧', '😮', '😲', '🤤', '😪', '😵', '🤐', '🥴', '🤢', '🤮', '🤧', '😷', '🤒',
                    '🤕', '🤑', '😈', '👿', '👹', '👺', '🤡', '💩', '👻', '💀', '☠', '️', '👽', '👾',
                    '🤖', '🎃', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
        await ctx.message.delete()
        if len(id) == 0:
            async for mess in ctx.message.channel.history(limit=1):
                for i in range(20):
                    emoji = emojis[random.randint(0, len(emojis)-1)]
                    await mess.add_reaction(emoji)
        else:
            try:
                print(id)
                mess = await ctx.fetch_message(int(id[0]))
                for i in range(20):
                    emoji = emojis[random.randint(0, len(emojis)-1)]
                    await mess.add_reaction(emoji)
            except:
                await ctx.send("not a valid id")




def setup(bot):
    bot.add_cog(Bomb_reactions(bot))
