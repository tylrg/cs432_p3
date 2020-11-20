import pymongo
from twython import Twython,TwythonError
import ssl
import math

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 
def compareUsers(sn,osn):
  client = pymongo.MongoClient("mongodb+srv://tgabrie2:cs432@cs432-p3.79oxz.mongodb.net/cs432?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
  db = client.cs432
  collection = db['test']

  ## get list of users in db
  cur = collection.find()
  #for doc in cur:
  #print(doc)
  #print(doc['_id'])

  # sn = "jaden"
  # ##compare with another user##
  # osn = "jaden"

  ##get all tweets for a given user
  #tweets = []
  # cur = collection.find({"_id": sn})
  # for doc in cur:
  #   #print(doc)
  #   print(doc['tweets'])


  ## delete a given user from the database
  # cur = collection.delete_one({"_id": sn})
  # print(cur)

  ### stats for similarity score ###
  snFollowing = []
  snAs = 0
  snSyntax = []
  osnFollowing = []
  osnAs = 0
  osnSyntax = []


  cur = collection.find({"_id": sn})
  for doc in cur:
    snFollowing = doc['following']
    snAs =  doc['avg_sentiment']
    snSyntax = doc['syntax_dict']

  cur = collection.find({"_id": osn})
  for doc in cur:
    osnFollowing = doc['following']
    osnAs =  doc['avg_sentiment']
    osnSyntax = doc['syntax_dict']

  sharedSyntax = len(intersection(snSyntax,osnSyntax)) # shared words between the two

  #print(len(intersection(snFollowing,osnFollowing)))
  avgFollowing = (len(snFollowing) + len(osnFollowing))/2

  sharedFollowing = (len(intersection(snFollowing,osnFollowing)))/ avgFollowing

  aSDiff = math.sqrt((snAs-osnAs)*(snAs-osnAs)) ## average sentiment for both users


  # Query twitter with the comma separated list

  APP_KEY = "UHz2Yr3qedZeNZxblgzqVbER6"
  APP_SECRET = "KavH3dnHPOPybPWBWXAWD7jAqfJRxDLqEK24N1m64O2fax0vM0"
  twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
  ACCESS_TOKEN = twitter.obtain_access_token()
  twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
  snOutput = twitter.lookup_user(screen_name=sn)[0]['id']
  osnOutput = twitter.lookup_user(screen_name=osn)[0]['id']

  inSN = -1
  inOSN = -1
  mutual = 0 ## do the users follow each other

  try:
    inSN = snFollowing.index(osnOutput)
    inOSN = osnFollowing.index(snOutput)
  except ValueError :
    mutual = 0


  if inSN > -1 and inOSN > -1:
    mutual = 1



  # print(sharedSyntax/30)
  # print(sharedFollowing)
  # print(aSDiff)
  # print(mutual)

  sScore = (sharedFollowing * 100)*(mutual+1)+(sharedSyntax/30)-aSDiff
  return sScore

