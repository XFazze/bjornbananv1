# https://pymongo.readthedocs.io/en/stable/tutorial.html
# https://docs.mongodb.com/mongodb-shell/reference/access-mdb-shell-help/


from pymongo import MongoClient, collation
import pymongo as pm
# connect to the mongodb server
client = MongoClient('localhost', 27017)

# connect to database / create(need to add collection and document too)
db = client.second_test

# connect to collection / create(need to add document too)
myCollection = db.test_myCollection


post = {"author": "sike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"]}

# create a document which also makes the database and collection exist
myCollection.insert_one(post)

print(myCollection.find_one())
print(myCollection.find_one({"author": "noel"}))

# id is not same as string id
docid = myCollection.find_one()['_id']
print(myCollection.find_one({"_id": docid}))

new_posts = [{"author": "Mike",
              "text": "Another post!",
              "number": 2,
              "tags": ["bulk", "insert"]},
             {"author": "Eliot",
              "title": "MongoDB is fun",
              "number": 5,
              "text": "and pretty easy too!"}]

# insert many in bulk 
result = myCollection.insert_many(new_posts)
print(result.inserted_ids)
print(myCollection.find_one({"_id": result.inserted_ids[0]}))


# find many 
for post in myCollection.find({"author": 'Eliot'}):
    print(post)

# count the documents
print(myCollection.count_documents({}))

# range queries when searching 
for post in myCollection.find({"number": {"$lt": 3}}).sort("author"):
    print(post)


# only unique profiles can be added to collection in order to avoid duplicates
result = db.profiles.create_index([('user_id', pm.ASCENDING)], unique=True)
sorted(list(db.profiles.index_information()))

# insert documents
user_profiles = [
    {'user_id': 211, 'name': 'Luke'},
     {'user_id': 212, 'name': 'Ziltoid'}]
result = db.profiles.insert_many(user_profiles)
print(result)