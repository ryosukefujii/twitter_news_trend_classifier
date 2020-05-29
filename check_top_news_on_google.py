import requests
from bs4 import BeautifulSoup


def check_links(q):
    # 参照ニュースサイトリスト
    news_sites = [
                    'headlines.yahoo.co.jp', # Yahooニュースヘッドライン
                    'news.yahoo.co.jp', # Yahooニュース
                    'news.livedoor.com', # livedoorニュース
                    'jiji.com', # 時事通信社
                    'nhk.or.jp', # NHK
                    'news.tbs.co.jp', # TBS
                    'news24.jp', # 日本テレビ
                    'newsweekjapan.jp', # News Week Japan
                    'asahi.com', # 朝日新聞
                    'mainichi.jp', # 毎日新聞
                    'nikkei.com', # 日経新聞
                    'chunichi.co.jp' # 中日新聞
                   ]

    # google search
    url = "https://www.google.co.jp/search"
    params = {"q": q}
    # User-Agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100"
    headers = {"User-Agent": user_agent}
    resp = requests.get(url, params=params, headers=headers)
    # 要素の抽出
    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select('.r > a') # class=r, <a>タグ
    links = []
    for item in items:
      links.append(item.get('href'))
    return links


# グーグル検索の１ページ目のURLを抽出し、時事ニュース関連かどうか判定する
def check_top_news(links):
    result_list = []
    for link in links:
      cnt = 0
      for news_site in news_sites:
        cnt += link.count(news_site)
      result_list.append(cnt)
    if sum(result_list) > 0:
      result = 'Top News'
    else:
      result = ''
    return result
