from twython import Twython
import pymongo
import pprint
import sys
import ssl
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime


def count_by_word(tweets_concat):
    word_counts = dict()
    words = tweets_concat.split()

    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    return sorted(word_counts.items(), key=lambda x: x[1], reverse=True)


APP_KEY = "UHz2Yr3qedZeNZxblgzqVbER6"
APP_SECRET = "KavH3dnHPOPybPWBWXAWD7jAqfJRxDLqEK24N1m64O2fax0vM0"
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)





#CODE TO GET TWEETS FOR A GIVEN USER and also calculate sentiment score
#print("\n\n\n\n")

sn = input('Enter Screen Name: ')
##sn = "drake"

analyzer = SentimentIntensityAnalyzer()
totalSentimentScore = 0
tweetCount = 0
compoundText = ""

tweets = []
try:
    user_timeline = twitter.get_user_timeline(screen_name= sn, count=30)
except TwythonError as e:
   print(e)
for tweet in user_timeline:
   tweetCount+=1
   sentiment_dict = analyzer.polarity_scores(tweet['text'])
   totalSentimentScore += sentiment_dict['compound']
   compoundText =  compoundText + " " + tweet['text']
   tweets.append(tweet);

#print(tweetCount)
syntax_dict = count_by_word(compoundText)


averageSentiment = totalSentimentScore/tweetCount;

## FOLLOWERS ##
followers = []
try:
    user_followers = twitter.get_followers_ids(screen_name = sn)
    followers = user_followers
    #print(len(followers['ids']))
except TwythonError as e:
   print(e)
# for friend in user_friends:
#    print (friend)


# FOLLOWING ##
following = []
try:
    user_friends = twitter.get_friends_ids(screen_name = sn)
    following = user_friends
    #print(len(following['ids']))
except TwythonError as e:
   print(e)
# for friend in user_friends:
#    print (friend)


lastUpdated = datetime.datetime.utcnow().isoformat()
syntax_dict = count_by_word(compoundText)
syntax_dict = list(filter(lambda x: x[1] != 1, syntax_dict))
userStore = {
   "_id": sn,
   "last_updated": lastUpdated,
   "avg_sentiment": averageSentiment,
   "syntax_dict": syntax_dict[:30],
   "following": following['ids'],
   "followers": followers['ids'],
   "tweets": tweets
}
#print(userStore)

client = pymongo.MongoClient("mongodb+srv://tgabrie2:cs432@cs432-p3.79oxz.mongodb.net/cs432?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
db = client.cs432
collection = db['test']
collection.insert_one(userStore)
# cur = collection.find()
# for doc in cur:
#   #print(doc)
#   print(doc['test_value'])



