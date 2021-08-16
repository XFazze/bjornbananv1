
from pymongo import MongoClient, collation
import pymongo as pm

client = MongoClient('localhost', 27017)
db = client.maindb

'''
name 'maindb'
database structure


- users
    {"_id" : mongodb id,
    "user_id" : dsicord id,
      }

management is part of guild variables now(config)
- guilds 
    {"_id" : mongodb id,
    "config" : {                                     CREATE THIS WITH ENABLE/DISABLE COMMAND
        "joinrole" : ['roleid'],
        "prefix" : ',',
        "bettervc" : ['channelid'],
        "delete_pinned" : {
            "guild_wide" : bool,
            "channels" : []
            },
        "deletingchannel" : ['channelid'],
        "joinleavemessage" : ['channelid'],,
        "bettervc" : ['channelid'],                  
    }
    "channels" : [                                       CREATE THIS WITH GUILDFIX WHICH IS CALLED AT TIMES
            {"_id" : mongodb id,
             "channelid" : channelid, 
             "name" : channelname,
             everything important here
             }]

mongodb extended reference pattern? how does it work
create multiple channel collections
- per channel messages 
    {"_id" : mongodb id,
    "messageid" : message,
    bulk stuff like messages

    }
- per channel deleted messages 
    {"_id" : mongodb id,
    "messageid" : message,
    bulk stuff like messages

    }

similar to tcstats/vcstats
- per channel tc logs
    {"_id" : mongodb id,
    "activitytype" : '1',
    }

- per channel vc logs
    {"_id" : mongodb id,
    "activitytype" : '1',
    }

- per guild joinleaves
    {"_id" : mongodb id,
    "activitytype" : '1',
    }

- per guild tickets
    {"_id" : mongodb id,
    "name" : 'userid',
    }



'''
