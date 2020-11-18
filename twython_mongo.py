from twython import Twython
import pymongo
import pprint
import sys
import ssl

APP_KEY = "UHz2Yr3qedZeNZxblgzqVbER6"
APP_SECRET = "KavH3dnHPOPybPWBWXAWD7jAqfJRxDLqEK24N1m64O2fax0vM0"
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

# client = pymongo.MongoClient("mongodb+srv://tgabrie2:cs432@cs432-p3.79oxz.mongodb.net/cs432?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
# db = client.cs432
# collection = db['test']
# cur = collection.find()
# for doc in cur:
#   #print(doc)
#   print(doc['test_value'])

print("\n\n\n\n")
sn = input('Enter Screen Name: ')

try:
    user_timeline = twitter.get_user_timeline(screen_name= sn, count=30)
except TwythonError as e:
   print(e)
for tweets in user_timeline:
   print (tweets['text'])

#print(s)