from pymongo import MongoClient
botName = 'ebot'

collection = MongoClient('localhost', 27017).maindb.tokens
myquery = {"botname": botName}
config = collection.find_one(myquery)

if config:
    print('found config', config)
else:
    print('creating token document')
    token = input('paste token here:')
    collection.insert_one(
        {
            'botName' : botName,
            'token' : token
        }
    )