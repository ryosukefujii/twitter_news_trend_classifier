コサイン類似度によるTwitterトレンドがニュース由来かどうか予測

【このnotebookについて】


【ゴール】
リアルタイムにTwitterトレンド50件をそれぞれがニュース由来のトレンドかどうか判定する。

【モデルの仕組み】
１）TwitterAPIを使ってトレンドツイートとニュースアカウントのツイートを取得
　・各ツイートはそれぞれ数十件を一つのテキストにまとめる。
２）データセットの前処理
　・正規表現など
３）分散表現の獲得
　・分散表現を獲得する
４）コサイン類似度を用いて判定する。
　・閾値を設定し、判定する。

【結果】
結果精度は７割り程度となった。

【その他試みたこと】


【利用するには】
・config.py ファイルにツイッターAPIトークンを記入

Requirement
・必要なツール、ライブラリ
$ pip install tweepy
$ pip install oseti
$ pip install requests requests_oauthlib
$ pip install sengiri
$ pip install gensim
$ pip install emoji
