# トレンドがニュース由来かどうかを予測

## 【このnotebookについて】
+ Twitterトレンドがニュース由来かどうかを分散表現を用いてコサイン類似度で予測する。
+ 正解ラベルは自動生成したかったので、グーグル検索結果より判定した物を使用。
### 【ゴール】
+ リアルタイムにTwitterトレンド30件程度取得し、それぞれニュース由来のトレンドかどうか判定する。

### 【モデルの仕組み】
1. TwitterAPIを使ってトレンドツイートとニュースアカウントのツイートを取得  
  + 各ツイートはそれぞれ数十件を一つのテキストにまとめる。
2. データセットの前処理
  + 正規表現など
3. 分散表現の獲得
  + 分散表現を獲得する
4. コサイン類似度を用いて判定する。
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
