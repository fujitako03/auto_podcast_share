import os
import re
from urllib import request

import requests
from bs4 import BeautifulSoup

API_KEY = os.getenv("YOUTUBE_API_KEY")
print(API_KEY)

def get_episode_url_all(broadcast_urls, episode_num):
    """複数ポッドキャストから指定した配信回のURLを取得する

    Args:
        broadcast_urls (dict): 各podcastの番組URL
        episode_num (string): エピソード番号（ex. #5, #6)

    Returns:
        dict: 指定した配信回の各ポッドキャストURL
    """

    epidode_urls = []
    # Apple
    service = "Apple"
    if broadcast_urls.get(service):
        epidode_urls.append({
            "service_name": service,
            "episode_url": get_episode_url_apple(broadcast_urls.get(service), episode_num)
        })
    else:
        pass

    # Spotify
    service = "Spotify"
    if broadcast_urls.get(service):
        epidode_urls.append({
            "service_name": service,
            "episode_url": get_episode_url_spotify(broadcast_urls.get(service), episode_num)
        })
    else:
        pass

    # stand.fm
    service = "stand.fm"
    if broadcast_urls.get(service):
        epidode_urls.append({
            "service_name": service,
            "episode_url": get_episode_url_standfm(broadcast_urls.get(service), episode_num)
        })
    else:
        pass

    # YouTube
    service = "YouTube"
    if broadcast_urls.get(service):
        epidode_urls.append({
            "service_name": service,
            "episode_url": get_episode_url_youtube(broadcast_urls.get(service), episode_num, API_KEY)
        })
    else:
        pass


    return epidode_urls

def get_episode_url_spotify(broadcast_url, episode_num):
    """spotifyの配信一覧URLから、該当エピソードのurlを取得する

    Args:
        broadcast_url (): 番組URL
        episode_num (string): エピソード番号（ex. #5, #6)

    Returns:
        string: 該当エピソードのurl
    """
    print("serch start "+episode_num+" in "+broadcast_url)
    # htmlをパース
    html = request.urlopen(broadcast_url)
    soup = BeautifulSoup(html,"html5lib")

    # エピソードリストを取得
    list_episode = soup.find_all(href=re.compile("episode"))
    # エピソードリストを取得
    for episode in list_episode:
        episode_text = episode.find("span", class_="track-name").text

        # 正規表現で判定
        if re.match(f"{episode_num}\s.+", episode_text):
            episode_url = episode.get('href') 
            return "https://open.spotify.com"+episode_url
        else:
            pass
    
    return "not_found"


def get_episode_url_apple(broadcast_url, episode_num):
    """Apple Podcastの配信一覧URLから、該当エピソードのurlを取得する

    Args:
        broadcast_url (): 番組URL
        episode_num (string): エピソード番号（ex. #5, #6)

    Returns:
        string: 該当エピソードのurl
    """
    print("serch start "+episode_num+" in "+broadcast_url)
    # htmlをパース
    html = request.urlopen(broadcast_url)
    soup = BeautifulSoup(html,"html5lib")
    
    # エピソードリストを取得
    list_episode = soup.find_all("li", class_="ember-view")

    # 指定した番号で始まるエピソードのurlを取得
    for episode in list_episode:
        episode_text = episode.find("a", class_="link tracks__track__link--block").text
        episode_text = episode_text.replace("\n", "").replace("      ","")

        # 正規表現で判定
        if re.match(f"{episode_num}\s.+", episode_text):
            episode_url = episode.find("a").get('href') 
            
            return episode_url
        else:
            pass

    return "not_found"

def get_episode_url_standfm(broadcast_url, episode_num):
    """Stand.fmの配信一覧URLから、該当エピソードのurlを取得する

    Args:
        broadcast_url (): 番組URL
        episode_num (string): エピソード番号（ex. #5, #6)

    Returns:
        string: 該当エピソードのurl
    """
    print("serch start "+episode_num+" in "+broadcast_url)
    # htmlをパース
    html = request.urlopen(broadcast_url)
    soup = BeautifulSoup(html,"html5lib")

    # エピソードリストを取得
    list_episode = soup.find_all(href=re.compile("episodes"))

    # 指定した番号で始まるエピソードのurlを取得
    for episode in list_episode[1:]:
        print("=="*30)
        episode_text = episode.find(
            class_="css-901oao css-cens5h r-190imx5 r-1b43r93 r-1od2jal r-rjixqe"
            ).text

        # 正規表現で判定
        if re.match(f"{episode_num}\s.+", episode_text):
            episode_url = episode.get("href") 

            return "https://stand.fm"+episode_url
        else:
            pass

    return "not_found"

def get_episode_url_youtube(channel_id, episode_num, apikey):
    """YouTubeの動画一覧ページから、該当エピソードのurlを取得する

    Args:
        broadcast_url (): YouTubeチャンネルの動画一覧URL
        episode_num (string): エピソード番号（ex. #5, #6)

    Returns:
        string: 該当エピソードのurl
    """
    base_url = 'https://www.googleapis.com/youtube/v3'
    url = base_url + '/search?key=%s&channelId=%s&part=snippet,id&order=date&maxResults=50'

    print("serch start "+episode_num+" in "+channel_id)
    # チャンネルの番組一覧を取得
    list_video = []
    while True:
        # チャンネル情報を取得
        print("start getting youtube url")
        response = requests.get(url % (apikey, channel_id))
        if response.status_code != 200:
            print('error')
            break
        result = response.json()

        # 動画情報をリストに格納
        list_video.extend([
            {
                "title": item['snippet']['title'],
                "video_id": item['id']['videoId'],
            }
            for item in result['items'] if item['id']['kind'] == 'youtube#video'
        ])

        # pagetokenの処理
        if 'nextPageToken' in result.keys():
            if 'pageToken' in url:
                url = url.split('&pageToken')[0]
            url += f'&pageToken={result["nextPageToken"]}'
        else:
            print('finish getting youtube url')
            break

    # 指定した番号で始まるエピソードのurlを取得
    for episode in list_video:
        episode_text = episode.get("title")

        # 正規表現で判定
        if re.match(f"{episode_num}\s.+", episode_text):
            video_id = episode.get("video_id") 
            return "https://www.youtube.com/watch?v="+video_id
        else:
            pass

    return "not_found"

if __name__=='__main__':
    episode_num="#5"
    broadcast_urls = {
        "Apple": "https://podcasts.apple.com/jp/podcast/%E3%82%B9%E3%82%AD%E3%83%9E%E3%82%B1%E3%82%A4%E3%82%AB%E3%82%AF/id1549488123",
        "Spotify": "https://open.spotify.com/show/4UAXC9FpPJMrOTQOdQUEDC",
        "stand.fm": "https://stand.fm/channels/60031bf7fc3475e2c8f7e457",
        "YouTube": "UCwzrfuQPgg-lCfbG6Qdt1Vw",
    }

    res = get_episode_url_all(broadcast_urls, episode_num=episode_num)
    print(res)
