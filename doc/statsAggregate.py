import discord
from pymongo import MongoClient
from discord.ext import commands
import matplotlib.pyplot as plt
import numpy as np
import pprint


collection = MongoClient('localhost', 27017).maindb.VCJoins
pipeline =  [{'$match': {'$and': [{'guildId': 802298523214938153}, {'time': {'gt': 1638996791.4233649}}]}}, {'$group': {'_id': '$userId', 'count': {'$sum': '$length'}}}]

data = list(collection.aggregate(pipeline))
pprint.pprint(data)
nd = [list(col) for col in zip(*[d.values() for d in data])]
print(nd)

#https://matplotlib.org/stable/plot_types/basic/bar.html#sphx-glr-plot-types-basic-bar-py