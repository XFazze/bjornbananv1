import discord
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get
import matplotlib.pyplot as plt
import numpy as np
import pprint


class vcStatsDisplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=[], enable=True)
    async def vctime(self, ctx, category='guildId'):
        await ctx.trigger_typing()
        # TODO add channel and cateogory
        collection = MongoClient('localhost', 27017).maindb.VCJoins
        timeframes = ['lifetime']
        for timeframe in timeframes:
            pipeline = [
                {
                    '$match': {
                        'guildId': 802298523214938153
                    }
                },
                {
                    '$group': {
                        "_id": "$userId",
                        "count": {
                            '$sum': '$length'
                        }
                    }

                }]

            data = list(collection.aggregate(pipeline))
            data = sorted(data, key = lambda i: i['count'],reverse=True)
            pprint.pprint(data)
            nd = [list(col) for col in zip(*[d.values() for d in data])]
            print(nd)
            fig, ax = plt.subplots()
            x = [get(self.bot.get_all_members(), id=d).name for d in nd[0]]
            y = [d/3600 for d in nd[1]]
            print(x, nd[1])

            ax.bar(x, y, width=0.7, edgecolor="white", linewidth=1)
            fig.autofmt_xdate(rotation=90)

            plt.savefig(f'static/plots/{category}-{timeframe}.jpg')
            embed = discord.Embed(
                title=f"Time spent in vc in {category[:-2]} in {timeframe}", color=0xFFF)
            with open(f'static/plots/{category}-{timeframe}.jpg', 'rb') as f:
                picture = discord.File(f)
                await ctx.reply(embed=embed, file=picture)


def setup(bot):
    bot.add_cog(vcStatsDisplay(bot))
