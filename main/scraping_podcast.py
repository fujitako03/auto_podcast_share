import re
from urllib import request

from bs4 import BeautifulSoup


def get_episode_url_all(broadcast_urls, episode_num):

    epidode_urls = {}
    # Apple
    service = "Apple"
    if broadcast_urls.get(service):
        epidode_urls[service] = get_episode_url_spotify(broadcast_urls.get(service), episode_num)
    else:
        epidode_urls[service] = ""

    # Spotify
    service = "Spotify"
    if broadcast_urls.get(service):
        epidode_urls[service] = get_episode_url_apple(broadcast_urls.get(service), episode_num)
    else:
        epidode_urls[service] = ""

    return epidode_urls

def get_episode_url_spotify(broadcast_url, episode_num):
    """spotifyのパースされたhtmlから、該当エピソードのurlを取得する

    Args:
        soup (): beautifulsoupeでパースされたhtml
        episode_num (string): エピソード番号（ex. #5, #6)

    Returns:
        string: 該当エピソードのurl
    """
    # htmlをパース
    html = request.urlopen(broadcast_url)
    soup = BeautifulSoup(html,"html5lib")

    # エピソードリストを取得
    list_episode = soup.find_all("li", class_="tracklist-row")
    for episode in list_episode:
        pattern = f"^{episode_num}\s.+"
        episode_text = episode.find("span", class_="track-name").text

        # 指定した番号で始まるエピソードのurlを取得
        if re.match(pattern, episode_text):
            episode_url = episode.find("a").get('href') 
            break
        else:
            episode_url = "/non"
            pass

    return "https://open.spotify.com"+episode_url

def get_episode_url_apple(soup, episode_num):
    """Appleのパースされたhtmlから、該当エピソードのurlを取得する

    Args:
        soup (): beautifulsoupeでパースされたhtml
        episode_num (string): エピソード番号（ex. #5, #6)

    Returns:
        string: 該当エピソードのurl
    """
    # htmlをパース
    html = request.urlopen(broadcast_url)
    soup = BeautifulSoup(html,"html5lib")

    # エピソードリストを取得
    list_episode = soup.find_all("li", class_="ember-view")
    for episode in list_episode:
        pattern = f"{episode_num}\s.+"
        episode_text = episode.find("a", class_="link tracks__track__link--block").text
        episode_text = episode_text.replace("\n", "").replace("      ","")

        # 指定した番号で始まるエピソードのurlを取得
        if re.match(pattern, episode_text):
            episode_url = episode.find("a").get('href') 
            break
        else:
            print("not match")
            episode_url="non"
            pass

    return episode_url

def get_episode_url_standfm(soup, episode_num):
    """Stand.fmのパースされたhtmlから、該当エピソードのurlを取得する

    Args:
        soup (): beautifulsoupeでパースされたhtml
        episode_num (string): エピソード番号（ex. #5, #6)

    Returns:
        string: 該当エピソードのurl
    """
    # htmlをパース
    html = request.urlopen(broadcast_url)
    soup = BeautifulSoup(html,"html5lib")

    # エピソードリストを取得
    list_episode = soup.find_all("li", class_="ember-view")
    for episode in list_episode:
        pattern = f"{episode_num}\s.+"
        episode_text = episode.find("a", class_="link tracks__track__link--block").text
        episode_text = episode_text.replace("\n", "").replace("      ","")

        # 指定した番号で始まるエピソードのurlを取得
        if re.match(pattern, episode_text):
            episode_url = episode.find("a").get('href') 
            break
        else:
            print("not match")
            pass

    return episode_url

if __name__=='__main__':
    episode_num="#5"
    broadcast_urls = {
        "Apple": "https://podcasts.apple.com/jp/podcast/%E3%82%B9%E3%82%AD%E3%83%9E%E3%82%B1%E3%82%A4%E3%82%AB%E3%82%AF/id1549488123",
        "Spotify": "https://open.spotify.com/episode/2a4czOt8QNlNS4NSckHfrl",
        "stand.fm": "https://stand.fm/channels/60031bf7fc3475e2c8f7e457",
    }

    res = get_episode_url_all(broadcast_urls, episode_num=episode_num)
    print(res)
