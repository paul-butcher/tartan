"""
Twitter bot for random Tartan
"""
import os
import tweepy

auth = tweepy.OAuthHandler(os.environ.get('KEY'), os.environ.get('SECRET'))
auth.set_access_token(os.environ.get('TOKEN'), os.environ.get('TOKEN_SECRET'))

api = tweepy.API(auth)
# threadcount = api.user_timeline('RandomTartan')[0].text
threadcount = 'B24 W4 B24 R2 K24 G24 W2'
print(threadcount)

def tweet_image():
    media_id = api.update_with_media('tartan.png', file=threadcount_to_png('')).media_id
    api.update_status(status='testing', media_ids=[media_id])

def threadcount_to_png(threadcount):
    pass

#tweet_image()
