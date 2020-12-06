# トレンドがニュース由来かどうかを予測

## 【このnotebookについて】
  + Twitterトレンドがニュース由来かどうかを分散表現を用いてコサイン類似度で予測する。
  + トレンドをグーグルで検索し、その検索結果より判定した値を正解ラベルとした。
### 【ゴール】
  + リアルタイムにTwitterトレンド30件程度取得し、それぞれニュース由来のトレンドかどうか判定する。

### 【モデルの仕組み】
1. Twitterトレンドの取得
  +   Twitter APIを用いてTwitterトレンドを取得
2. トレンドツイートの取得、テキスト化
  +   トレンドに関して呟いている最新ツイートを数十件程度取得し、一つのテキストにまとめる。（トレンドテキスト）
3. ニュースアカウントのツイートの取得  
  + ニュースメディアの最新ツイートを数十件程度取得し、一つのテキストにまとめる。（ニューステキスト）
4. テキスト前処理
  + トレンドテキストおよびニューステキストを正規表現などで加工する。
5. 分散表現の獲得
  + 加工したテキストをUniversal Sentence Encoderを用いて分散表現を獲得する。
6. コサイン類似度を用いた予測
  + 2つの分散表現のコサイン類似度を算出する。
  + 閾値（0.3）を用いて二値分類で予想結果を出力する。
7. 予測の結果の取得
  + トレンドに対してグーグル検索を行い、１ページ目に表示されるリンクのリスト取得する。
  + 取得したリストに対して、予め用意したニュースメディアのURLリストに一致した場合をニュース由来のトレンドとする正解ラベルを作成し、予測結果と照合させ精度を検証する。  


### 【結果】
+ 結果精度は75%程度となった。


### 【その他試みたこと】
キーワードに関するトップニュースがある場合、グーグル検索結果の上部に表示されるが、それをスクレイピングで取得しようとしたがうまく取得できなかった。


### 【利用するには】
+ config.py ファイルを作成しツイッターAPIトークンを設定する。
+ config.py ファイルを **twitter_news_trend_classifierフォルダ** 直下に配置する。

```
consumer_key = 'XXXXXXXXXX'
consumer_secret = 'XXXXXXXXXX'
access_token = 'XXXXXXXXXX'
access_token_secret = 'XXXXXXXXXX'
```

+ **Twitter_News_Trend_Classifier.pyファイル**を実行する


### 【Requirement】
必要なツール、ライブラリ
```
$ pip install mecab-python3
$ pip install oseti
$ pip install emoji
$ pip install tensorflow-hub
$ pip install tensorflow-text
$ pip install requests_oauthlib
$ pip install tweepy
$ pip install beautifulsoup4
```
