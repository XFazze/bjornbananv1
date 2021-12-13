import discord
#from ..admin.managecommands import perms
import json
from discord import member
from discord import user
from discord import embeds
from pymongo import MongoClient, collation
from discord.ext import commands, tasks
from discord.utils import get
import time, random
import pymongo as pm

def fillBracket(depth, randomusers):
    if 2**depth < len(randomusers):
        matches = fillBracket(depth+1, randomusers)
        newmatches = []
        for i in range(int(len(matches)/2)):
            newmatches.append({
                'user1' : matches[i],
                'user2' : matches[i+int(len(matches)/2)],
                'winner' : None
            })
        return newmatches

    else:
        lenOfRandomUsers = len(randomusers) 
        if lenOfRandomUsers % 2 != 0:
            empty_match = True
            lenOfRandomUsers -= 1


        matches = []
        for userIndex in range(int(2**depth/2)):
            matches.append({
                'user1' : randomusers[userIndex],
                'user2' : None,
                'winner' : None
            })
        print('matches', matches)
        del randomusers[0:int(2**depth/2)]

        splitSize = depth/len(randomusers)
        for i in range(len(randomusers)):
            pos = round(splitSize*i)
            matches[pos]['user2'] = randomusers[i]

        for match in matches:
            print(match['user1'],match['user2'])
        return matches
        
def sendlayer(ctx, brackets, bracketChannel):
    if not brackets:
        return
    print('==new layer==')
    if 'discord' in brackets['user1'].keys():
        print(brackets)

    else:
        sendlayer(ctx, brackets['user1'], bracketChannel)
        sendlayer(ctx, brackets['user2'], bracketChannel)



class tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# TODO unsingup function
# Tournament
    # create the tournament
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def createTournament(self, ctx, role:discord.Role = None):
        author = ctx.author.id

        if member == None:
            await ctx.reply(embed=discord.Embed(title="You didnt provide a valid role.", color=0xFD3333))


        collection = MongoClient('localhost', 27017).maindb.tournaments
        tournamentId = random.randint(1000,9999)
        while collection.find_one({'id': tournamentId}):
            tournamentId = random.randint(1000,9999)
        
        name = "admin"+str(tournamentId)
        signup = await ctx.channel.category.create_text_channel(name)
        await signup.set_permissions(role, read_messages=True)
        await signup.set_permissions(ctx.guild.default_role, read_messages=False)
        
        name = "signup"+str(tournamentId)
        signup = await ctx.channel.category.create_text_channel(name)
        await signup.set_permissions(role, read_messages=True)
        await signup.set_permissions(ctx.guild.default_role, read_messages=False)


        name = 'brackets'+str(tournamentId)
        brackets = await ctx.channel.category.create_text_channel(name)
        await brackets.set_permissions(role, read_messages=True,send_messages=True)
        await brackets.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)

        name = 'playerlist'+str(tournamentId)
        playerlist = await ctx.channel.category.create_text_channel(name)
        await playerlist.set_permissions(role, read_messages=True,send_messages=True)
        await playerlist.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)


        tournament = {
            'id' : tournamentId,
            'creator' : author,
            'guild' : ctx.guild.id,
            'date' : time.asctime(),
            'signupChannel' : signup.id,
            'bracketsChannel': brackets.id,
            'playerlistChannel': playerlist.id,
            'categoryId' : ctx.channel.category.id,
            'role' : role.id,
            'users' : [],
            'signup' : True,
            'brackets': None

        }
        collection.insert_one(tournament)
        title = "Successfully created tournament #"+str(tournamentId)
        await ctx.reply(embed=discord.Embed(title=title, color=0x00FF42))
        await self.updateplayerlist()

    # sign up 
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name[:6] != 'signup' or message.author == self.bot.user:
            return

        collection = MongoClient('localhost', 27017).maindb.tournaments
        tournament = collection.find_one({'id': int(message.channel.name[6:10])})
        if not tournament['signupChannel']:
            await message.reply(embed=discord.Embed(title="Sign ups are closed.", color=0xFD3333))
            return
        change = False
        for user in tournament['users']:
            if user['discord'] == message.author.id and user['username'] == message.content:
                await message.reply(embed=discord.Embed(title="You already singed up with this username.", color=0x00FF42))
                return

            elif user['username'] == message.content:  
                doubleuser = get(self.bot.get_all_members(), id=user['discord'])
                title = "Username already signed up from another discord account: "+doubleuser.name+'#'+str(doubleuser.discriminator)+'. Contact admin if needed.'
                await message.reply(embed=discord.Embed(title=title, color=0xFD3333))
                return

            elif user['discord'] == message.author.id:
                change = True
                tmpuser = user

        if change:
            tmpuser['username'] = message.content
            tournament = collection.replace_one({'id': int(message.channel.name[6:10])}, tournament)
            await message.reply(embed=discord.Embed(title="You have changed your username.", color=0x00FF42))
            await self.updateplayerlist()
            return

        newUser = {
            'discord' : message.author.id,
            'username' : message.content
        }
        tournament['users'].append(newUser)

        collection.replace_one({'id': int(message.channel.name[6:10])}, tournament)
        await message.reply(embed=discord.Embed(title="You have signed up.", color=0x00FF42))
        await self.updateplayerlist()
        
    # close sign ups
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def closeSignUps(self, message):
        collection = MongoClient('localhost', 27017).maindb.tournaments
        tournament = collection.find_one({'id': int(message.channel.name[5:9])})
        if not tournament['signupChannel']:
            await message.reply(embed=discord.Embed(title="Sign ups are already closed.", color=0xFD3333))
            return
        tournament['signupChannel'] = False
        tournament = collection.replace_one({'id': int(message.channel.name[5:9])}, tournament)
        await message.reply(embed=discord.Embed(title="Closed sign ups.", color=0x00FF42))

    # close sign ups
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def openSignUps(self, message):
        collection = MongoClient('localhost', 27017).maindb.tournaments
        tournament = collection.find_one({'id': int(message.channel.name[5:9])})
        if tournament['signupChannel']:
            await message.reply(embed=discord.Embed(title="Sign ups are already open.", color=0xFD3333))
            return
        tournament['signupChannel'] = True
        collection.replace_one({'id': int(message.channel.name[5:9])}, tournament)
        await message.reply(embed=discord.Embed(title="Opened sign ups.", color=0x00FF42))

    # create brackets
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def createBrackets(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.tournaments
        tournament = collection.find_one({'id': int(ctx.channel.name[5:9])})
        if tournament['signupChannel']:
            tournament['signupChannel'] = False
            await ctx.reply(embed=discord.Embed(title="Closed sign ups.", color=0x00FF42))
        if len(tournament['users']) < 2:
            await ctx.reply(embed=discord.Embed(title="Not more than 1 player signed up", color=0xFD3333))
            return

        randomusers = []
        for user in tournament['users']:
            randomusers.insert(random.randint(0, len(randomusers)), user)
        
        brackets = fillBracket(1, randomusers)[0]
        tournament['brackets'] = brackets
        collection.replace_one({'id': int(ctx.channel.name[5:9])}, tournament)

        await ctx.reply(embed=discord.Embed(title="Created brackets", color=0x00FF42))

        # create 2 spots
        # check if you have more than 2 users
        # if not fill and retujrn
        # else create 2 new spots for every spot
        
  
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def fakeusers(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.tournaments
        tournament = collection.find_one({'id': int(ctx.channel.name[5:9])})
        for i in range(13):
            tournament['users'].append({
            'discord' : str(random.randint(1000,9999)),
            'username' : str(random.randint(1000,9999))
        })
        collection.replace_one({'id': int(ctx.channel.name[5:9])}, tournament)
        await ctx.reply(embed=discord.Embed(title="Created 5 fake usrs.", color=0x00FF42))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def sendbracket(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.tournaments
        tournament = collection.find_one({'id': int(ctx.channel.name[5:9])})
        bracketChannel = self.bot.get_channel(tournament['bracketsChannel'])
        print('Starting recursion==============================\n\n')
        sendlayer(ctx, tournament['brackets'], bracketChannel)


    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def sendplayerlist(self, ctx):
        collection = MongoClient('localhost', 27017).maindb.tournaments
        tournament = collection.find_one({'id': int(ctx.channel.name[5:9])})
        playerlistChannel = self.bot.get_channel(tournament['playerlistChannel'])

        embed=discord.Embed(title="Playerlist", color=0x00FF42)
        for user in tournament['users']:
            doubleuser = get(self.bot.get_all_members(), id=user['discord'])
            name = doubleuser.name+"#"+doubleuser.discriminator
            embed.add_field(name=name, value=user['username'], inline=False)
        
        await playerlistChannel.purge(limit=100)
        await playerlistChannel.send(embed=embed)


    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def updateplayerlist(self):
        collection = MongoClient('localhost', 27017).maindb.tournaments
        tournaments = collection.find()
        for tournament in tournaments:
            try:
                playerlistChannel = self.bot.get_channel(tournament['playerlistChannel'])

                embed=discord.Embed(title="Playerlist", color=0x00FF42)
                for user in tournament['users']:
                    guild =  self.bot.get_guild(tournament['guild'])
                    doubleuser = guild.get_member(user['discord'])
                    name = doubleuser.name+"#"+doubleuser.discriminator
                    embed.add_field(name=name, value=user['username'], inline=False)

                await playerlistChannel.purge(limit=100)
                await playerlistChannel.send(embed=embed)
            except:
                pass



# on message signup
# if started
# if discord user already has singpuped
# if username already signuped
# signup

# create  brackets

# start

# win lose report

# advance



def setup(bot):
    bot.add_cog(tournament(bot))
