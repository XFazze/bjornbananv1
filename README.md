# Björnbanan
This bot is an all-around discordbot with varius purposes. 
[The invite link with administrative priveliges.](https://discord.com/oauth2/authorize?client_id=759541425078534154&permissions=8&scope=bot)

## Functions [all commands](https://fabbe90.gq/bjornbanan/commands)
* Moderation commands
  * User managment
  * Logging features
  * Ticket system
* Custom channels
  * Voice channels adapting to demand
  * Auto deleting channels
* Role managment
  * Reaction roles
  * Auto role when user joins
* User-friendly information commands



# Nucleus
https://discord.com/oauth2/authorize?client_id=775007176157954058&scope=bot&permissions=8589934591


# Setup

## Prerequsiteies
* MongoDB (v4 or later should be good) [install on ubuntu](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)
* Python3
* ```sudo apt-get install python3-git```
* pm2(npm)

## discord token setup
1. Add a database 'maindb'.
2. To that db add a collection 'tokens'.
3. Insert {'botName':'bbot', 'token':yourDiscordToken'} into that collection

## Run the bot
```python3 bbot.py```
use the command ,reloadall in a dicord channel with the bot to load the cogs

## Run bot as without terminal open
[guide](https://www.vultr.com/docs/how-to-run-a-python-discord-bot-on-ubuntu-21-04/)
```
pm2 start bbot.py --interpreter=/usr/bin/python3
```
