
from pymongo import MongoClient, collation
import pymongo as pm

client = MongoClient('localhost', 27017)
db = client.maindb
mycollection = db.guilds

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
    "name" : name
    "id" : id,
    "settings" : {
        "commandname" : {
            "guild" : [roleid],
            "channel" : [
                {"channelid" : channelid,
                "roleid" : [roleid]}
                    ]
                } 
    "config" : {                                    
        "joinrole" : ['roleid'],
        "prefix" : ',',
        "bettervc" : ['category_id'],
        "delete_pinned" : [channelid]
        "deletingchannel" : ['channelid'],
        # "joinleavemessage" : ['channelid']         
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

    }
- per channel edit messages 
    {"_id" : mongodb id,
    "messageid" : message,

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
