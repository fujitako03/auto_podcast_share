import os

import main.models
from main import db
from main.models import Broadcast, Podcast

# dbの削除
path_db = "./main/podcast.db"
if os.path.exists(path_db):
    os.remove(path_db)

# db作成
main.models.init()

# データを挿入
podcast = Podcast(
    podcast_id="1",
    podcast_url="https://anchor.fm/s/4779d744/podcast/rss",
    podcast_name="スキマケイカク",
    )
db.session.add(podcast)
db.session.commit()

# データを挿入
broadcast = Broadcast(
    broadcast_url="https://podcasts.apple.com/jp/podcast/%E3%82%B9%E3%82%AD%E3%83%9E%E3%82%B1%E3%82%A4%E3%82%AB%E3%82%AF/id1549488123",
    broadcast_service="Apple",
    podcast_id="1",
    )
db.session.add(broadcast)
db.session.commit()

# データを挿入
broadcast = Broadcast(
    broadcast_url="https://open.spotify.com/show/4UAXC9FpPJMrOTQOdQUEDC",
    broadcast_service="Spotify",
    podcast_id="1",
    )
db.session.add(broadcast)
db.session.commit()

# 結果の出力
entries = Broadcast.query.all()
print(entries)
