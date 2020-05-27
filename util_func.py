import datetime
import re
import MeCab
import oseti
import emoji


# 日付設定
def get_now():
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
#now = now.strftime('%Y-%m-%d_%H:%M:%S_JST')
    return now

# データ取得期間設定
def get_until_and_since(days=0, hours=12, minutes=0, seconds=0, until=None):
    if until==None:
        until = get_now()
    days = datetime.timedelta(days=days)
    hours = datetime.timedelta(hours=hours)
    minutes = datetime.timedelta(minutes=minutes)
    seconds = datetime.timedelta(seconds=seconds)
    since = until - days - hours - minutes - seconds
    until, since = until.strftime('%Y-%m-%d_%H:%M:%S_JST'), since.strftime('%Y-%m-%d_%H:%M:%S_JST')
    return until, since

# # twitter api 日本時間表記
#   def jp_time(created_at):
#     return created_at + datetime.timedelta(hours=9)



# トレンドテキスト前処理
# ツイートテキスト整形

# # 自然言語処理
#   # 絵文字除去
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

# 分かち書き
def wakati_gaki(text):
    mecab = MeCab.Tagger ("-Owakati")
    return mecab.parse(text)

def preprocess_text(text):
    text = remove_url(text)
    text = remove_mention_and_hashtag(text)
    text =  remove_emoji(text)
    return text


#ハッシュタグ取得
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
