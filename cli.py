import pymongo
from twython import Twython,TwythonError
import ssl
import math
import dateutil.parser
import pprint
import sys
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

def addUserToDB(sn):
    APP_KEY = "UHz2Yr3qedZeNZxblgzqVbER6"
    APP_SECRET = "KavH3dnHPOPybPWBWXAWD7jAqfJRxDLqEK24N1m64O2fax0vM0"
    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

    analyzer = SentimentIntensityAnalyzer()
    totalSentimentScore = 0
    tweetCount = 0
    compoundText = ""

    tweets = []
    try:
        user_timeline = twitter.get_user_timeline(screen_name= sn, count=30)
    except TwythonError as e:
        print(e)
        return False

    for tweet in user_timeline:
        tweetCount+=1
        sentiment_dict = analyzer.polarity_scores(tweet['text'])
        totalSentimentScore += sentiment_dict['compound']
        compoundText =  compoundText + " " + tweet['text']
        tweets.append(tweet);

    syntax_dict = count_by_word(compoundText)

    averageSentiment = 0
    if tweetCount != 0:
        averageSentiment = totalSentimentScore/tweetCount;

    ## FOLLOWERS ##
    followers = []
    try:
        user_followers = twitter.get_followers_ids(screen_name = sn)
        followers = user_followers
    except TwythonError as e:
        print(e)
        return False

    following = []
    try:
        user_friends = twitter.get_friends_ids(screen_name = sn)
        following = user_friends
    except TwythonError as e:
        print(e)
        return False


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


    client = pymongo.MongoClient("mongodb+srv://tgabrie2:cs432@cs432-p3.79oxz.mongodb.net/cs432?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
    db = client.cs432
    collection = db['test']
    collection.insert_one(userStore)

    return True

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


def menu(user, collection):
    print(f"-------------\n*USER: @{user}*\n-------------\
          \n1: View This User's Data\n2: View This User's Tweets\n3: Compare Two Screen Names\n4: Find Similar Sentiment Scores To This User\n5: Delete This User\
          \n6: Refresh Data For This User\n7: Sign Out\n0: Exit CLI")
    choice = input('Choose an action: ')
    clear()
    if(choice == '1'):
        cur = collection.find({'_id': user})
        print(f'-------------\nVIEW OPTIONS\n-------------\
              \n1: Header Data\n2: View Following\n3: View Followers\n')
        choice = input('Choose an action: ')
        clear()

        if(choice == '1'):
            for doc in cur:
                date = dateutil.parser.parse(doc['last_updated'])
                print()
                print(f'--------------------\nUSER: {user}\nSENTIMENT SCORE: {doc["avg_sentiment"]}\nLAST UPDATED: {date}\
                      \n--------------------\nMOST USED WORDS\n--------------------')
                if(len(doc['syntax_dict']) == 0):
                    print('HAS NEVER TWEETED')
                else:
                    for i, word in enumerate(doc['syntax_dict']):
                        print('#'+str(i+1)+f': {word}')
                break;
            menu(user, collection)
        elif(choice == '2'):
            for doc in cur:
                print('--------------------\nFOLLOWING\n--------------------')
                if(len(doc['following']) == 0):
                    print('NOT FOLLOWING ANYONE')
                else:
                    n = 1
                    print(f'Page {n}\n--------------------')
                    st = ''
                    for fol in doc['following'][(n-1) * 10 : (n)*10]:
                        st+=(f'{fol}, ')
                    print(st[:-2]+'\n')
                    print('Next: 1, Back: 2, Exit: 0')
                    choice = input('Enter an action: ')

                    while(True):
                        clear()
                        if(choice=='1'):
                            if((len(doc['following']))-(n*10)>0):
                                n+=1
                            else:
                                print('ALREADY AT LAST PAGE')
                        elif(choice=='2'):
                            if(n==1):
                                print('ALREADY AT FIRST PAGE')
                            else:
                                n-=1
                        elif(choice=='0'):
                            break
                        else:
                            print('NOT A VALID CHOICE')

                        print('--------------------\nFOLLOWING\n--------------------')
                        print(f'Page {n}\n--------------------')
                        st = ''
                        for fol in doc['following'][(n-1) * 10 : (n)*10]:
                            st+=(f'{fol}, ')
                        print(st[:-2]+'\n')
                        print('Next: 1, Back: 2, Exit: 0')
                        choice = input('Enter an action: ')
                break
            menu(user, collection)
        elif(choice == '3'):
            for doc in cur:
                print('--------------------\nFOLLOWERS\n--------------------')
                if(len(doc['followers']) == 0):
                    print('NO FOLLOWERS\n')
                else:
                    n = 1
                    print(f'Page {n}\n--------------------')
                    st = ''
                    for fol in doc['followers'][(n-1) * 10 : (n)*10]:
                        st+=(f'{fol}, ')
                    print(st[:-2]+'\n')
                    print('Next: 1, Back: 2, Exit: 0')
                    choice = input('Enter an action: ')

                    while(True):
                        clear()
                        if(choice=='1'):
                            if((len(doc['followers']))-(n*10)>0):
                                n+=1
                            else:
                                print('ALREADY AT LAST PAGE')
                        elif(choice=='2'):
                            if(n==1):
                                print('ALREADY AT FIRST PAGE')
                            else:
                                n-=1
                        elif(choice=='0'):
                            break
                        else:
                            print('NOT A VALID CHOICE')

                        print('--------------------\nFOLLOWERS\n--------------------')
                        print(f'Page {n}\n--------------------')
                        st = ''
                        for fol in doc['followers'][(n-1) * 10 : (n)*10]:
                            st+=(f'{fol}, ')
                        print(st[:-2]+'\n')
                        print('Next: 1, Back: 2, Exit: 0')
                        choice = input('Enter an action: ')
                break
            menu(user, collection)
        else:
            print('NOT A VALID CHOICE')
            menu(user, collection)

    elif(choice == '2'):
        print(f'--------------------\n{user}\'s TWEETS\n--------------------')
        cur = collection.find({'_id': user})
        for doc in cur:
            for i, tweet in enumerate(doc['tweets']):
                print('TWEET #'+str(i+1))
                date = dateutil.parser.parse(tweet['created_at'])
                outputText = tweet["text"].strip('\n').strip('\t')
                print(f'\t--------------------\n\tTWEETED AT: {date}\
                      \n\tTWEET ID: {tweet["id_str"]}\
                      \n\tRETWEETS: {tweet["retweet_count"]}\n\tFAVORITES: {tweet["favorite_count"]}\n\t--------------------')
                print(f'\tTWEET BODY: {outputText}\n\t--------------------')
            break
        menu(user, collection)
    elif(choice == '3'):
        user1 = input('Enter a screen name: ')
        user2 = input('Enter another screen name: ')
        clear()
        cur = collection.find({'_id': user1})
        cur2 = collection.find({'_id': user2})
        if(len(list(cur))==0):
            print('FIRST SCREEN NAME NOT IN DATABASE')
            menu(user, collection)
        elif(len(list(cur2))==0):
            print('SECOND SCREEN NAME NOT IN DATABASE')
            menu(user, collection)
        else:
            score = compareUsers(user1, user2)
            print(f'SIMILARITY SCORE OF @{user1} AND @{user2}: {score}')
            menu(user, collection)
    elif(choice == '4'):
        curU = collection.find({'_id': user})
        userSent = 0
        for doc in curU:
            userSent = doc['avg_sentiment']
            break
        closests = []

        cur = list(collection.find({}).sort([("avg_sentiment", pymongo.ASCENDING)]))
        for i, doc in enumerate(cur):
            if(i==len(cur)-1 and len(cur)>2 and doc['avg_sentiment']==userSent):
                closests.append({'_id': cur[i-1]['_id'], 'avg_sentiment': cur[i-1]['avg_sentiment']})
                closests.append({'_id': cur[i-2]['_id'], 'avg_sentiment': cur[i-2]['avg_sentiment']})
                break
            if(doc['avg_sentiment'] > userSent):
                if(i==0):
                    closests.append({'_id': cur[i]['_id'], 'avg_sentiment': cur[i]['avg_sentiment']})
                    closests.append({'_id': cur[i+1]['_id'], 'avg_sentiment': cur[i+1]['avg_sentiment']})
                elif(i==len(cur)-1):
                    closests.append({'_id': cur[i]['_id'], 'avg_sentiment': cur[i]['avg_sentiment']})
                    closests.append({'_id': cur[i-2]['_id'], 'avg_sentiment': cur[i-2]['avg_sentiment']})
                else:
                    closests.append({'_id': cur[i]['_id'], 'avg_sentiment': cur[i]['avg_sentiment']})
                    closests.append({'_id': cur[i-2]['_id'], 'avg_sentiment': cur[i-2]['avg_sentiment']})
                break
        print(f"--------------------\nSIMILAR SENTIMENT SCORES\n@{user}'s SENTIMENT SCORE: {userSent}\n--------------------\
              \nUSER: @{closests[0]['_id']}\nAVG SENTIMENT SCORE: {closests[0]['avg_sentiment']}\n--------------------\
              \nUSER: @{closests[1]['_id']}\nAVG SENTIMENT SCORE: {closests[1]['avg_sentiment']}")
        menu(user, collection)
    elif(choice == '5'):
        collection.delete_many({'_id': user})
        print(f'DELETED {user}\nSIGNED OUT {user}')
        main()
    elif(choice == '6'):
        collection.delete_many({'_id': user})
        addUserToDB(user)
        print(f"REFRESHED @{user}'s DATA")
        menu(user, collection)
    elif(choice == '7'):
        print(f'SIGNED OUT {user}')
        main()
    elif(choice == '0'):
        quit()
    else:
        print('NOT A VALID CHOICE')
        menu(user, collection)

def clear():
    print('\033c', end='')

def main():
  print('-------------\n*TITLE HERE*\n-------------\
        \n1: Grab a Twitter User\n0: Exit\n')
  choice = input('Choose an action: ')
  clear()
  if(choice == '1'):
      user = input('Enter a twitter username: ')
      client = pymongo.MongoClient("mongodb+srv://jwhite48:cs432@cs432-p3.79oxz.mongodb.net/cs432?retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
      db = client.cs432
      collection = db['test']
      cur = collection.find()
      grabUser = True
      for doc in cur:
        if(doc['_id'] == user):
            grabUser = False
            break
      clear()
      if(grabUser):
          if(addUserToDB(user)):
              print('ADDED USER TO DATABASE WITH TWITTER INFO')
          else:
              main()
      else:
          print('USER ALREADY IN DATABASE')

      menu(user, collection)
  elif(choice == '0'):
      quit()
  else:
      print('NOT A VALID CHOICE')
      main()
  client.close()

main()

# OPTIONS #
# 1 sign in (username, password)
# 2 view user data (authenticated?)(just make sure signed in)
# 2a view tweets (no arg)
# 2b view sentiment score (no arg)
# 2c view last updated (no arg)
# 3. compare to other users (username,other_username)
# 4 find similar scores (no arg)
# 5 remove data (no arg)
# 6 refresh data
# 7 sign out
# 0 exit
