import config # ツイッターAPIトークン取得
import util_func as uf # 自作関数モジュール呼び出し
import tweepy
import numpy as np
from requests_oauthlib import OAuth1Session
import json

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret
twitter = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)
# tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True) # 利用禁止期間の解除を待機後に実行する


class GetTweetFromTrend:
    def __init__(self, n_trends, woe_id=23424856):

  # Twitter API
        self.n_trends = n_trends # トレンド取得数
        self.woe_id = woe_id # エリアID


# twitter api トレンドリスト取得
    def get_trends(self):
        trends = api.trends_place(id=self.woe_id) # id = 23424856 # The Yahoo! Where On Earth ID
        text = None
        trend_list = []
        for trend in trends[0]["trends"]:
            trend_list.append(trend["name"])
        trend_list =  trend_list[:self.n_trends]
        return trend_list


    def get_text_list(self, n_tweets=30):
        trend_list = self.get_trends()
        trend_text_list = []
        until, since = uf.get_until_and_since()
        for q in trend_list:
            text = ''
            for tweet in tweepy.Cursor(api.search, q=q, result_type='latest', since=since, until=until).items(n_tweets):
                text += tweet.text
                text = uf.preprocess_text(text)
            trend_text_list.append(text)
        return trend_text_list


# Twitterニュースメディアアカウントのリスト
news_media = [
                'Sankei_news',
                'HuffPostJapan',
                'mainichijpnews',
                'nhk_news',
                ]


# Twitterニュースメディアアカウントのからツイートを集め1つのテキストにする
class GetTweetFromNews:
    def __init__(self, n_news_tweet=30):
        self.n_news_tweet = n_news_tweet

# 最新ニュースツイート取得
    def get_text_list(self):
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json" #タイムライン取得エンドポイント
        until, since = uf.get_until_and_since()
        for media in news_media:
          params ={'count' : self.n_news_tweet, 'id' : news_media, 'since':since} #取得数
          res = twitter.get(url, params=params)
          timelines = json.loads(res.text)
          text = ''
          for line in timelines:
            text += line['text']
            text += ' '
        text = uf.preprocess_text(text)
        return text


# # トレンド取得
#   self.trend_list = self.get_trends(self.n_trends, self.id)
#   self.trend_tweet_list = []
#   for i, q in enumerate(trend_list):
#       self.trend_tweet_list.append(get_text_from_tweets(q, items=n_tweets)) # 各トレンドのツイートをitems数取得して結合
