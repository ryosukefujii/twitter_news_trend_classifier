#!/usr/bin/env python
# coding: utf-8


import config # ツイッターAPIトークン取得
import tweepy
import datetime
import numpy as np
import pandas as pd
import json
from requests_oauthlib import OAuth1Session
pd.set_option("display.max_columns", 100)
pd.set_option('display.max_rows', 5000)
import re
import MeCab
import oseti
import emoji
import gensim
from gensim.models import KeyedVectors


consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret
twitter = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True) # 利用禁止期間の解除を待機後に実行する



now = datetime.datetime.now() + datetime.timedelta(hours=9)
week_ago = now - datetime.timedelta(days=7)
now, week_ago = now.strftime('%Y-%m-%d_%H:%M:%S_JST'), week_ago.strftime('%Y-%m-%d_%H:%M:%S_JST')

# # オリジナル関数

# ## 時間設定


# 現在の時刻を取得
def get_now():
  now = datetime.datetime.now() + datetime.timedelta(hours=9)
  #now = now.strftime('%Y-%m-%d_%H:%M:%S_JST')
  return now

# Until・Sinceの取得
def get_until_and_since(days=0, hours=0, minutes=0, seconds=0, until=get_now()):
  days = datetime.timedelta(days=days)
  hours = datetime.timedelta(hours=hours)
  minutes = datetime.timedelta(minutes=minutes)
  seconds = datetime.timedelta(seconds=seconds)
  since = until - days - hours - minutes - seconds
  until, since = until.strftime('%Y-%m-%d_%H:%M:%S_JST'), since.strftime('%Y-%m-%d_%H:%M:%S_JST')
  return until, since

# 日本時間表記
def jp_time(created_at):
  return created_at + datetime.timedelta(hours=9)

get_until_and_since(7) # 検索期間の設定


# ## トレンド

# ### トレンドリスト取得

def get_trends(n_trends=50, id=23424856):
  trends = api.trends_place(id=id) # id = 23424856 # The Yahoo! Where On Earth ID
  text = None
  trend_list = []
  for trend in trends[0]["trends"]:
    trend_list.append(trend["name"])
  return trend_list[:n_trends]


# ### ハッシュタグ取得

# def get_hashtags():
#   # hashtag_list
#   hashtag_list = []
#   hashtags = tweet.entities["hashtags"]
#   for hashtag in hashtags:
#     hashtag_list.append(hashtag['text'])
#   # retweeted_status_list
#   retweeted_hashtag_list = []
#   try:
#     hashtags = tweet.retweeted_status.entities["hashtags"]
#     for hashtag in hashtags:
#       retweeted_status_list.append(hashtag['text'])
#   except AttributeError:
#     pass
#   return hashtag_list, retweeted_hashtag_list


# ## 自然言語処理

# ### URL除去

# 絵文字除去
def remove_emoji(text):
  return ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in text])

# URL除去
def remove_url(text):
  return re.sub(r'(http|https)://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?', "", text)

# メンション・ハッシュタグ除去
def remove_mention_and_hashtag(text):
  rt = r'RT\s.*?\s'
  mention = r'@.*?\s'
  hashtag = r'#.*?\s|#\s.*?'
  full_width_space = r'\u3000'
  line_break = r'\n'
  pattern = rt + '|' + mention + '|' + hashtag + '|' + full_width_space + '|' + line_break
  p = re.compile(pattern)
  result = p.sub('', text)
  return result

# ### 分かち書き
def wakati_gaki(text):
  mecab = MeCab.Tagger ("-Owakati")
  return mecab.parse(text)


# # トレンドテキスト前処理

# ### テキスト前処理


# ツイートテキスト整形
def preprocess_text(text):
  text = remove_url(text)
  text = remove_mention_and_hashtag(text)
  text =  remove_emoji(text)
  return text

def get_text_from_tweets(q, items=50):
  until, since = get_until_and_since(days=0, hours=12, minutes=0, seconds=0, until=get_now()) # 検索期間の設定
  text = ''
  for tweet in tweepy.Cursor(api.search, q=q, result_type='latest', since=since, until=until).items(items):
    text += tweet.text
  text = preprocess_text(text)
  return text


# ### 最新ニュースツイート取得
def check_news_tweet(news_media, news_cnt):
  url = "https://api.twitter.com/1.1/statuses/user_timeline.json" #タイムライン取得エンドポイント
  until, since = get_until_and_since(days=0, hours=12, minutes=0)
  for media in news_media:
    params ={'count' : news_cnt, 'id' : media, 'since':since} #取得数
    res = twitter.get(url, params=params)
    timelines = json.loads(res.text)
    text = ''
    for line in timelines:
      text += line['text']
      text += ' '
  text = preprocess_text(text)
  return text

news_media = ['Sankei_news', 'HuffPostJapan', 'mainichijpnews']


# # 類似度比較
def check_sim(text1, text2):
  import tensorflow_hub as hub
  import numpy as np
  import tensorflow_text

  # for avoiding error
  import ssl
  ssl._create_default_https_context = ssl._create_unverified_context

  def cos_sim(v1, v2):
      return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

  embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")
  texts = [tweet_text, news_text]
  vectors = embed(texts)
  return cos_sim(vectors[0], vectors[1])

def judge_trend(result, threshold):
  if result > threshold:
    return 'Positive'
  else:
    return 'Negative'
# パラメータ
n_trends = 10
n_tweets = 30
news_cnt = 40
threshold = 0.3 # 判定閾値

print('----- 設定 -----')
print('自動 → Press [0] or Any')
print('手動 → Press [1]')

try:
  setting = int(input())
except ValueError:
  setting = 0

if setting == 1:
  print('取得するトレンド件数は？(デフォルト：10件)')
  n_trends = int(input())
  print('トレンドから取得するツイート件数は？(デフォルト：' + str(n_tweets) +'件)')
  n_tweets = int(input())
  print('メディアから取得するツイート件数は？(デフォルト：' + str(news_cnt) +'件)')
  news_t_cnt = int(input())
  print('判定する際の類似度の閾値は？(デフォルト' + str(threshold) + ')')
  threshold = float(input()) # 判定閾値
else:
  pass

print()
print('----- 設定内容 -----')
print('取得するトレンド件数', n_trends, '件')
print('トレンドから取得するツイート件数：', n_tweets, '件')
print('ニュースメディア：', news_media)
print('メディアから取得するツイート件数：', news_cnt, '件')
print('閾値：', threshold)
print('-----------------------')

# print('----- 判定開始 -----')
trend_list = get_trends(n_trends=n_trends, id=23424856) # トレンドリスト取得
news_text = check_news_tweet(news_media, news_cnt) # ニュースメディアからツイート取得
for i, q in enumerate(trend_list):
  tweet_text = get_text_from_tweets(q, items=n_tweets) # 各トレンドのツイートをitems数取得して結合
  result = check_sim(tweet_text, news_text) # 各トレンドツイートとニュースメディアのツイートの類似度を算出
  print(i, q, result, judge_trend(result, threshold))


print('----- 判定開始 -----')
data_list = ['key word', 'sim', 'pred', 'label', 'result']
df = pd.DataFrame(columns=data_list)
trend_list = get_trends(n_trends=n_trends, id=23424856) # トレンドリスト取得
news_text = check_news_tweet(news_media, news_cnt) # ニュースメディアからツイート取得
for i, q in enumerate(trend_list):
  tweet_text = get_text_from_tweets(q, items=n_tweets) # 各トレンドのツイートをitems数取得して結合
  result = check_sim(tweet_text, news_text) # 各トレンドツイートとニュースメディアのツイートの類似度を算出
  pred = np.where(result > threshold, 1, 0)
  print(q)
  label = int(input())
  df.loc[i] = i, q, result, pred, label, int(pred==label)


print((df.result == 1).sum()/df.shape[0], '%')
display(df)
