from twython import Twython

APP_KEY = "here"
APP_SECRET = "here"
OAUTH_TOKEN = "here"
OAUTH_TOKEN_SECRET = "here"

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

retrieved_user_tweets = twitter.get_user_timeline(user_id="kanyewest")