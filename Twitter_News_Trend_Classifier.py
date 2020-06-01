#!/usr/bin/env python
# coding: utf-8
import get_tweet
from get_tweet import GetTweetFromTrend
from get_tweet import GetTweetFromNews
import check_top_news_on_google as ggl
import numpy as np
import pandas as pd
pd.set_option("display.max_columns", 100)
pd.set_option('display.max_rows', 5000)
# pd.set_option('display.unicode.east_asian_width', True)
from IPython.display import display
# import json


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
  texts = [text1, text2]
  vectors = embed(texts)
  return cos_sim(vectors[0], vectors[1])

def judge_trend(result, threshold):
  text = '予想：'
  if result > threshold:
    return text + 'ニュース由来'
  else:
    return text + 'その他'

def preds(result, threshold):
  if result > threshold:
    return 1
  else:
    return 0

def get_result(pred, g_result):
  if pred == g_result:
    return 1
  else:
    return 0

# パラメータ
n_trends = 10
n_tweets = 30
n_news_tweet = 40
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
  print('メディアから取得するツイート件数は？(デフォルト：' + str(n_news_tweet) +'件)')
  news_t_cnt = int(input())
  print('判定する際の類似度の閾値は？(デフォルト' + str(threshold) + ')')
  threshold = float(input()) # 判定閾値
else:
  pass

print()
print('----- 設定内容 -----')
print('取得するトレンド件数：', n_trends, '件')
print('トレンドから取得するツイート件数：', n_tweets, '件')
print('ニュースメディア：', get_tweet.news_media)
print('メディアから取得するツイート件数：', n_news_tweet, '件')
print('閾値：', threshold)
print('-----------------------')

# print('----- 判定開始 -----')
# data_list = ['key word', 'sim', 'pred']
# df = pd.DataFrame(columns=data_list)
# trend_list = get_trends(n_trends=n_trends, id=23424856) # トレンドリスト取得
# news_text = check_news_tweet(news_media, news_cnt) # ニュースメディアからツイート取得
# for i, q in enumerate(trend_list):
#   tweet_text = get_text_from_tweets(q, items=n_tweets) # 各トレンドのツイートをitems数取得して結合
#   sim = check_sim(tweet_text, news_text) # 各トレンドツイートとニュースメディアのツイートの類似度を算出
#   judge = judge_trend(sim, threshold)
#   df.loc[i] = q, sim, judge
#   print(i, q, sim, judge)
trend_tweets = GetTweetFromTrend(n_trends)
trends = trend_tweets.get_trends()
trend_text_list = trend_tweets.get_text_list(n_tweets)
news_tweets = GetTweetFromNews(n_news_tweet)
news_text = news_tweets.get_text_list()

data_list = ['キーワード', '類似度', '予想', 'トップニュース', '正解']
# data_list = ['key word', 'sim', 'pred', 'label', 'result']
df = pd.DataFrame(columns=data_list)

for i , (trend, tweet) in enumerate(zip(trends, trend_text_list)):
    sim = check_sim(tweet, news_text)
    judge = judge_trend(sim, threshold)
    pred = preds(sim, threshold)
    search_links = ggl.check_links(trend)
    g_result, top_news = ggl.check_top_news(search_links)
    result = get_result(pred, g_result)
    # print(i, trend, sim, judge, top_news)
    df.loc[i] = [trend, sim, pred, g_result, result]

from tabulate import tabulate
print(tabulate(df, tablefmt="grid"))
accuracy = (df['正解'] == 1).sum()/df.shape[0]
print(accuracy*100, '%')
