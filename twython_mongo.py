from twython import Twython
import pymongo
import pprint
import sys
import ssl

APP_KEY = "here"
APP_SECRET = "here"
OAUTH_TOKEN = "here"
OAUTH_TOKEN_SECRET = "here"

client = pymongo.MongoClient("mongodb+srv://tgabrie2:cs432@cs432-p3.79oxz.mongodb.net/cs432?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
db = client.cs432
collection = db['test']
cur = collection.find()
for doc in cur:
  #print(doc)
  print(doc['test_value'])

# print("twython")
# twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# retrieved_user_tweets = twitter.get_user_timeline(user_id="kanyewest")

