import requests
from bs4 import BeautifulSoup

def check_top_news(q):
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
    title_text = soup.get_text()
    item = soup.select('.e2BEnf.U7izfe > h3') # Top stories = トップニュース
    try:
        result = 'Top stories' in item[0]
    except IndexError:
        item = 'None'
        result = 'Top stories' in item[0]
    return result
