import pymongo

client = pymongo.MongoClient("mongodb+srv://tgabrie:cs432@cs432-p3.79oxz.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test
