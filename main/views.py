
from flask import redirect, render_template, request, url_for

from main import app, db
from main.models import Broadcast, Podcast
from main.modules.scraping_podcast import get_episode_url_all


@app.route('/')
def show_podcasts():
    podcasts = Podcast.query.all()
    broadcasts = Broadcast.query.all()

    return render_template(
        'podcasts.html',
        podcasts=podcasts, 
        broadcasts=broadcasts,
        episode_num="#",
        episode_urls="",
        )


@app.route('/add-boardcast', methods=['POST'])
def add_broadcast():
    broadcast = Broadcast(
        podcast_id = request.form['podcast_id'],
        broadcast_url = request.form['broadcast_url'],
        broadcast_service = request.form['broadcast_service']
    )
    db.session.add(broadcast)
    db.session.commit()

    return redirect(url_for('show_podcasts'))


@app.route('/get_episode_url', methods=['POST'])
def get_episode_url():
    # フォームの値を取得
    episode_num = "#"+request.form['episode_num'][0]
    print(episode_num)
    
    # 配信先一覧を取得
    podcasts = Podcast.query.all()
    broadcasts = Broadcast.query.all()

    # 配信先 url
    broadcast_urls = {}

    for br in broadcasts:
        broadcast_urls[br.broadcast_service] = br.broadcast_url

    # エピソードのurlを取得
    episode_urls = get_episode_url_all(broadcast_urls, episode_num)

    return render_template(
        'podcasts.html',
        podcasts=podcasts, 
        broadcasts=broadcasts,
        episode_num=episode_num,
        episode_urls=episode_urls
        )

