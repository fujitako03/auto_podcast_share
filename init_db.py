import logging
import os

from main import db
from main.models.models import Broadcast, Podcast, init


def init_db():

    # dbの削除
    path_db = "./main/podcast.db"
    if os.path.exists(path_db):
        os.remove(path_db)

    # db作成
    init()

    logging.info("start create db")
    # データを挿入
    podcast = Podcast(
        podcast_url="https://anchor.fm/s/4779d744/podcast/rss",
        podcast_name="スキマケイカク",
        )
    db.session.add(podcast)
    db.session.commit()

    # データを挿入
    broadcast = Broadcast(
        broadcast_service="Apple",
        broadcast_url="https://podcasts.apple.com/jp/podcast/%E3%82%B9%E3%82%AD%E3%83%9E%E3%82%B1%E3%82%A4%E3%82%AB%E3%82%AF/id1549488123",
        podcast_id="1",
        )
    db.session.add(broadcast)
    db.session.commit()

    # データを挿入
    broadcast = Broadcast(
        broadcast_service="Spotify",
        broadcast_url="https://open.spotify.com/show/4UAXC9FpPJMrOTQOdQUEDC",
        podcast_id="1",
        )
    db.session.add(broadcast)
    db.session.commit()

    # データを挿入
    broadcast = Broadcast(
        broadcast_service="stand.fm",
        broadcast_url="https://stand.fm/channels/60031bf7fc3475e2c8f7e457",
        podcast_id="1",
        )
    db.session.add(broadcast)
    db.session.commit()

    # データを挿入
    broadcast = Broadcast(
        broadcast_service="YouTube",
        broadcast_url="UCwzrfuQPgg-lCfbG6Qdt1Vw",
        podcast_id="1",
        )
    db.session.add(broadcast)
    db.session.commit()

    # 結果の出力
    entries = Broadcast.query.all()
    print(entries)

if __name__=='__main__':
    init_db()
