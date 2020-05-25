# Twitterトレンドがニュース由来かどうかを予測

## 【このnotebookについて】
+ コサイン類似度によるTwitterトレンドがニュース由来かどうか予測する。

### 【ゴール】
+ リアルタイムにTwitterトレンド50件をそれぞれがニュース由来のトレンドかどうか判定する。

### 【モデルの仕組み】
1. TwitterAPIを使ってトレンドツイートとニュースアカウントのツイートを取得  
 + 各ツイートはそれぞれ数十件を一つのテキストにまとめる。
1. データセットの前処理
 + 正規表現など
1. 分散表現の獲得
 + 分散表現を獲得する
1. コサイン類似度を用いて判定する。
 + 閾値を設定し、判定する。
<br/>

### 【結果】
+ 結果精度は７割程度となった。

### 【その他試みたこと】


### 【利用するには】
+ config.py ファイルにツイッターAPIトークンを記入

```
consumer_key = 'XXXXXXXXXX'
consumer_secret = 'XXXXXXXXXX'
access_token = 'XXXXXXXXXX'
access_token_secret = 'XXXXXXXXXX'
```

### 【Requirement】
必要なツール、ライブラリ
```
$ pip install mecab-python3
$ pip install oseti
$ pip install emoji
$ pip install tensorflow_text
$ pip install requests_oauthlib
```
