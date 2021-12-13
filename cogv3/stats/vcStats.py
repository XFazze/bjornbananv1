import discord
from pymongo import MongoClient
from discord.ext import commands, tasks
import time
from datetime import datetime


class vcStatsLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        #print(member)
        #print(before)
        #print(after)
# join
        if not before.channel: # join channel
            collection = MongoClient('localhost', 27017).maindb.VCtempJoins
            doc = {
                'action' : 'join',
                'userId' : member.id,
                'userName':f'{member.name}#{member.discriminator}',
                'channel' : after.channel.id,
                'category' : after.channel.category_id,
                'guildId' : after.channel.guild.id,
                'time': time.time(),
                'date' : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'joinUsersInChannel' : len(after.channel.members)-1
            }
            collection.insert_one(doc)

        elif not after.channel: # left channel
            collection = MongoClient('localhost', 27017).maindb.VCtempJoins
            query = {'userId' : member.id, 'action':'join'}
            doc = collection.find_one(query)
            if not doc: # something went wrong
                print('error in vcstats leaveing')
                return
            collection.remove(query)

            doc['length'] = time.time() - doc['time']
            if doc['length']  < 60:
                return
            doc['leaveUsersInChannel'] = len(before.channel.members)

            collection = MongoClient('localhost', 27017).maindb.VCJoins
            collection.insert_one(doc)

        elif after.channel != before.channel: # user moved
            collection = MongoClient('localhost', 27017).maindb.VCtempJoins
            query = {'userId' : member.id, 'action':'join'}
            doc = collection.find_one(query)
            if not doc: # something went wrong
                print('error in vcstats moving')
                return
            collection.remove(query)

            doc['length'] = time.time() - doc['time']
            if doc['length']  < 60:
                return
            doc['leaveUsersInChannel'] = len(before.channel.members)

            collection = MongoClient('localhost', 27017).maindb.VCJoins
            collection.insert_one(doc)


            collection = MongoClient('localhost', 27017).maindb.VCtempJoins
            doc = {
                'action' : 'join',
                'userId' : member.id,
                'userName':f'{member.name}#{member.discriminator}',
                'channel' : after.channel.id,
                'category' : after.channel.category_id,
                'guildId' : after.channel.guild.id,
                'time': time.time(),
                'date' : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'joinUsersInChannel' : len(before.channel.members)
            }
            collection.insert_one(doc)

# self deaf
        elif after.self_deaf != before.self_deaf:
            if after.self_deaf:
                collection = MongoClient('localhost', 27017).maindb.VCtempSelfDeaf
                doc = {
                    'action' : 'selfDeaf',
                    'userId' : member.id,
                    'userName':f'{member.name}#{member.discriminator}',
                    'channel' : after.channel.id,
                    'category' : after.channel.category_id,
                    'guildId' : after.channel.guild.id,
                    'time': time.time(),
                    'date' : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    'usersInChannel' : len(after.channel.members)
                }
                collection.insert_one(doc)

            elif before.self_deaf:
                collection = MongoClient('localhost', 27017).maindb.VCtempSelfDeaf
                query = {'userId' : member.id, 'action':'selfDeaf'}
                doc = collection.find_one(query)
                if not doc: # something went wrong
                    print('error in vcstats selfDeaf')
                    return
                collection.remove(query)

                doc['length'] = time.time() - doc['time']
                if doc['length'] < 60:
                    return
                doc['leaveUsersInChannel'] = len(before.channel.members)

                collection = MongoClient('localhost', 27017).maindb.VCSelfDeaf
                collection.insert_one(doc)

# self mute
        elif after.self_mute != before.self_mute:
            if after.self_mute:
                collection = MongoClient('localhost', 27017).maindb.VCtempSelfMute
                doc = {
                    'action' : 'SelfMute',
                    'userId' : member.id,
                    'userName':f'{member.name}#{member.discriminator}',
                    'channel' : after.channel.id,
                    'category' : after.channel.category_id,
                    'guildId' : after.channel.guild.id,
                    'time': time.time(),
                    'date' : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    'usersInChannel' : len(after.channel.members)
                }
                collection.insert_one(doc)

            if before.self_mute:
                collection = MongoClient('localhost', 27017).maindb.VCtempSelfMute
                query = {'userId' : member.id, 'action':'SelfMute'}
                doc = collection.find_one(query)
                if not doc: # something went wrong
                    print('error in vcstats SelfMute')
                    return
                collection.remove(query)

                doc['length'] = time.time() - doc['time']
                if doc['length']  < 60:
                    return
                doc['leaveUsersInChannel'] = len(before.channel.members)

                collection = MongoClient('localhost', 27017).maindb.VCSelfMute
                collection.insert_one(doc)

# stream
        elif after.self_stream != before.self_stream:
            if after.self_stream:
                collection = MongoClient('localhost', 27017).maindb.VCtempStream
                doc = {
                    'action' : 'Stream',
                    'userId' : member.id,
                    'userName':f'{member.name}#{member.discriminator}',
                    'channel' : after.channel.id,
                    'category' : after.channel.category_id,
                    'guildId' : after.channel.guild.id,
                    'time': time.time(),
                    'date' : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    'usersInChannel' : len(after.channel.members)
                }
                collection.insert_one(doc)

            if before.self_stream:
                collection = MongoClient('localhost', 27017).maindb.VCtempStream
                query = {'userId' : member.id, 'action':'Stream'}
                doc = collection.find_one(query)
                if not doc: # something went wrong
                    print('error in vcstats Stream')
                    return
                collection.remove(query)

                doc['length'] = time.time() - doc['time']
                if doc['length']  < 60:
                    return
                doc['leaveUsersInChannel'] = len(before.channel.members)

                collection = MongoClient('localhost', 27017).maindb.VCStream
                collection.insert_one(doc)

# admin mute
        elif after.mute != before.mute:
            if after.mute:
                collection = MongoClient('localhost', 27017).maindb.VCtempAdminMute
                doc = {
                    'action' : 'AdminMute',
                    'userId' : member.id,
                    'userName':f'{member.name}#{member.discriminator}',
                    'channel' : after.channel.id,
                    'category' : after.channel.category_id,
                    'guildId' : after.channel.guild.id,
                    'time': time.time(),
                    'date' : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    'usersInChannel' : len(after.channel.members)
                }
                collection.insert_one(doc)

            if before.mute:
                collection = MongoClient('localhost', 27017).maindb.VCtempAdminMute
                query = {'userId' : member.id, 'action':'AdminMute'}
                doc = collection.find_one(query)
                if not doc: # something went wrong
                    print('error in vcstats AdminMute')
                    return
                collection.remove(query)

                doc['length'] = time.time() - doc['time']
                if doc['length']  < 60:
                    return
                doc['leaveUsersInChannel'] = len(before.channel.members)

                collection = MongoClient('localhost', 27017).maindb.VCAdminMute
                collection.insert_one(doc)

# admin deaf
        elif after.deaf != before.deaf:
            if after.deaf:
                collection = MongoClient('localhost', 27017).maindb.VCtempAdminDeaf
                doc = {
                    'action' : 'AdminDeaf',
                    'userId' : member.id,
                    'userName':f'{member.name}#{member.discriminator}',
                    'channel' : after.channel.id,
                    'category' : after.channel.category_id,
                    'guildId' : after.channel.guild.id,
                    'time': time.time(),
                    'date' : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    'usersInChannel' : len(after.channel.members)
                }
                collection.insert_one(doc)

            if before.deaf:
                collection = MongoClient('localhost', 27017).maindb.VCtempAdminDeaf
                query = {'userId' : member.id, 'action':'AdminDeaf'}
                doc = collection.find_one(query)
                if not doc: # something went wrong
                    print('error in vcstats AdminDeaf')
                    return
                collection.remove(query)

                doc['length'] = time.time() - doc['time']
                if doc['length']  < 60:
                    return
                doc['leaveUsersInChannel'] = len(before.channel.members)

                collection = MongoClient('localhost', 27017).maindb.VCAdminDeaf
                collection.insert_one(doc)

# video
        elif after.self_video != before.self_video:
            if after.self_video:
                collection = MongoClient('localhost', 27017).maindb.VCtempVideo
                doc = {
                    'action' : 'Video',
                    'userId' : member.id,
                    'userName':f'{member.name}#{member.discriminator}',
                    'channel' : after.channel.id,
                    'category' : after.channel.category_id,
                    'guildId' : after.channel.guild.id,
                    'time': time.time(),
                    'date' : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    'usersInChannel' : len(after.channel.members)
                }
                collection.insert_one(doc)
                
            if before.self_video:
                collection = MongoClient('localhost', 27017).maindb.VCtempVideo
                query = {'userId' : member.id, 'action':'Video'}
                doc = collection.find_one(query)
                if not doc: # something went wrong
                    print('error in vcstats Video')
                    return
                collection.remove(query)

                doc['length'] = time.time() - doc['time']
                if doc['length']  < 60:
                    return
                doc['leaveUsersInChannel'] = len(before.channel.members)

                collection = MongoClient('localhost', 27017).maindb.VCVideo
                collection.insert_one(doc)



def setup(bot):
    bot.add_cog(vcStatsLogger(bot))