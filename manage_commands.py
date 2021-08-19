# Enable/disable command

    @commands.group(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx):
        if ctx.invoked_subcommand is None:
            if len(ctx.message.content.split(" ")) == 1:
                await ctx.send(embed=discord.Embed(title="Provide a command", color=0xFD3333))
                return
            print("disable called")

            command = ctx.message.content.split(" ")[1]
            validcommand = False
            for cmd in self.bot.commands:
                if command == cmd.name:
                    validcommand = True
                    break
            if not validcommand:
                await ctx.send(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
                return

            collection = MongoClient('localhost', 27017).maindb.guilds
            myquery = {"id": ctx.guild.id}
            settings = collection.find_one(myquery)["settings"]
            if command not in settings.keys():
                settings[command] = {
                    "guild": False,
                    "category": [],
                    "disabled_category": [],
                    "channel": [],
                    "disabled_channel": []
                }

            if settings[command]['guild']:
                settings[command]['guild'] = False
                newvalue = {"$set": {"settings": settings}}
                collection.update_one(myquery, newvalue)
                await ctx.send(embed=discord.Embed(title="Disabled "+command+" on server", color=0x00FF42))
            else:
                await ctx.send(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))

    @disable.command(pass_context=True)
    async def category(ctx, category: discord.CategoryChannel = None, command: str = None):
        print("disable category ", category, command)
        validcommand = False
        for cmd in self.bot.commands:
            if command == cmd.name:
                validcommand = True
                break

        if not validcommand:
            await ctx.send(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
            return
        print(command)
        collection = MongoClient('localhost', 27017).maindb.guilds
        myquery = {"id": ctx.guild.id}
        settings = collection.find_one(myquery)["settings"]
        if command not in settings.keys():
            settings[command] = {
                "guild": False,
                "category": [],
                "disabled_category": [],
                "channel": [],
                "disabled_channel": []
            }

        if category.id not in settings[command]['disabled_category']:
            settings[command]['disabled_category'].append(category.id)
            if category.id in settings[command]['category']:
                settings[command]['category'].remove(category.id)
            newvalue = {"$set": {"settings": settings}}
            collection.update_one(myquery, newvalue)
            await ctx.send(embed=discord.Embed(title="Disabled "+command+" in category " + category.name, color=0x00FF42))
        else:
            await ctx.send(embed=discord.Embed(title="Command is already disabled", color=0xFD3333))

    @disable.command(pass_context=True)
    async def channel(ctx, channel: discord.TextChannel = None, command: str = None):
        print("disabling channel called ", channel, command)

    @commands.group(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx):
        if ctx.invoked_subcommand is None:
            if len(ctx.message.content.split(" ")) == 1:
                await ctx.send(embed=discord.Embed(title="Provide a command", color=0xFD3333))
                return
            print("enable called")

            command = ctx.message.content.split(" ")[1]
            validcommand = False
            for cmd in self.bot.commands:
                if command == cmd.name:
                    validcommand = True
                    break
            if not validcommand:
                await ctx.send(embed=discord.Embed(title="Provide a valid command", color=0xFD3333))
                return

            collection = MongoClient('localhost', 27017).maindb.guilds
            myquery = {"id": ctx.guild.id}
            settings = collection.find_one(myquery)["settings"]
            if command not in settings.keys():
                settings[command] = {
                    "guild": False,
                    "category": [],
                    "disabled_category": [],
                    "channel": [],
                    "disabled_channel": []
                }

            if not settings[command]['guild']:
                settings[command]['guild'] = True
                newvalue = {"$set": {"settings": settings}}
                collection.update_one(myquery, newvalue)
                await ctx.send(embed=discord.Embed(title="Enabled "+command+" on server", color=0x00FF42))
            else:
                await ctx.send(embed=discord.Embed(title="Command is already enabled", color=0xFD3333))

    @enable.command(pass_context=True)
    async def category(ctx, category: discord.CategoryChannel = None, command: str = None):
        print("Enabling category ", category, command)

    @enable.command(pass_context=True)
    async def channel(ctx, channel: discord.TextChannel = None, command: str = None):
        print("Enabling channel ", channel, command)
