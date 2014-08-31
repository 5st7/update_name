#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import tweepy
from tweepy import Stream, TweepError
import logging
import urllib

import json
import random

import re

CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

class CustomStreamListener(tweepy.StreamListener):
	
	def on_data(self, data):
		try:
			raw_data = data
			data = json.loads(data)
			ta = tweepy.API(auth)
			if "text" in data:
				if self.is_reply(data):
					match = re.search(r'.+update_name\s*(.*)', data['text'])
					if match is not None:
						#print 'matched!'
						#new_screen_name = u'れみゅ～@' + match.group(1)
						new_screen_name = match.group(1)

						#name length have to more 0 and lower 20

						print '------------'
						print 'Will update name \"' + new_screen_name + '\"'
						tweet = u'@' + data['user']['screen_name'] + u' ' + new_screen_name + u'に改名させられました（仮）'
						ta.update_profile(name=new_screen_name)
						ta.update_status(tweet)

		except Exception, e:
			print "Exception:" + str(e) 	
	
	def is_reply(self, data):
		if "in_reply_to_screen_name" in data:
			return data['in_reply_to_screen_name'] == 'foolish_remew'
		return False

	def on_error(self, status_code):
		print >> sys.stderr, 'Encountered error with status code:', status_code
		return True #Don't kill the stream

	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True #Don't kill the stream

class UserStream(Stream):

	def user_stream(self, follow=None, track=None, async=False, locations=None):
		self.parameters = {"delimited":"length",}
		self.headers['Content-type'] = "application/x-www-form-urlencoded"

		if self.running:
			raise TweepError('Stream object already connected!')

		self.scheme = "https"
		self.host = "userstream.twitter.com"
		self.url = "/1.1/user.json"

		if follow:
			self.parameters['follow'] = ','.join(map(str, follow))
		if track:
			self.parameters['track'] = ','.join(map(str, track))
		if locations and len(locations) > 0:
			assert len(locations) % 4 == 0
			self.parameters['locations'] = ','.join(['%.2f' % l for l in locations])

		self.body = urllib.urlencode(self.parameters)
		logging.debug("[User Stream URL]:%s://%s%s" % (self.scheme, self.host, self.url))
		logging.debug("[Request Body]:" + self.body)
		self._start(async)

def main():
	stream = UserStream(auth, CustomStreamListener())
	stream.timeout = None
	stream.user_stream()

if __name__ == "__main__":
	main()

