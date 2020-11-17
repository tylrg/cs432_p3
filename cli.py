import pymongo
import ssl
import datetime

def menu(user, collection):
    print(f'-------------\n*USER: {user}*\n-------------\
          \n1: View User\n2: View Tweets\n3: Compare to Other Users\n4: Find Similar Scores\n5: Remove Data\
          \n6: Refresh Data\n7: Sign Out\n0: Exit')
    choice = input('Choose an action: ')
    clear()
    if(choice == '1'):
        cur = collection.find({'_id': user})
        for doc in cur:
            date = datetime.datetime.strptime(doc['last_updated'],'%Y-%m-%dT%H:%M+%SZ')
            print()
            print(f'--------------------\nUSER: {user}\nSENTIMENT SCORE: {doc["avg_sentiment"]}\nLAST UPDATED: {date.strftime("%b %d %Y %H:%M:%S")}\
                  \n--------------------\nMOST USED WORDS\n--------------------')
            if(len(doc['syntax_dict']) == 0):
                print('HAS NEVER TWEETED')
            else:
                for i, word in enumerate(doc['syntax_dict']):
                    print('#'+str(i+1)+f': {word}')
            print('--------------------\nFOLLOWING\n--------------------')
            if(len(doc['following']) == 0):
                print('NOT FOLLOWING ANYONE')
            else:
                st = ''
                for fol in doc['following']:
                    st+=fol+', '
                print(st[:-2])
            print('--------------------\nFOLLOWERS\n--------------------')
            if(len(doc['followers']) == 0):
                print('NO FOLLOWERS\n')
            else:
                st = ''
                for fol in doc['followers']:
                    st+=fol+', '
                print(st[:-2]+'\n')
            break
        menu(user, collection)    
    elif(choice == '2'):
        print(f'--------------------\n{user}\'s TWEETS\n--------------------')
        cur = collection.find({'_id': user})
        for doc in cur:
            for i, tweet in enumerate(doc['tweets']):
                print('TWEET #'+str(i+1))
                date = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
                print(f'\t--------------------\n\tTWEETED AT: {date.strftime("%Y-%m-%d %H:%M:%S")}\
                      \n\tTWEET ID: {tweet["id_str"]}\n\t--------------------')
                print(f'\tTWEET BODY: {tweet["text"]}\n\t--------------------')
            break
        menu(user, collection)
    elif(choice == '3'):
        print('')
    elif(choice == '4'):
        print('')
    elif(choice == '5'):
        cur = collection.delete_many({'_id': user})
        print(f'DELETED {user}\nSIGNED OUT {user}')
        main()
    elif(choice == '6'):
        print('')
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
          print('GRABBED USER') #or print user doesnt exist
          #do Tyler code for grabbing from twitter
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
