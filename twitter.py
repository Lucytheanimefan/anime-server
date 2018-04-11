import tweepy
from os import environ


TWITTER_CONSUMER_KEY = environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN_KEY = environ.get('TWITTER_ACCESS_TOKEN_KEY')
TWITTER_ACCESS_TOKEN_SECRET = environ.get('TWITTER_ACCESS_TOKEN_SECRET')


class AnimeTweeter:
	def __init__(self):
		self.auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
		self.api = tweepy.API(self.auth, parser=tweepy.parsers.JSONParser())

	def search_hashtag(self, query, limit):
		return self.api.search(q=query, lang="en", count=limit)["statuses"]



