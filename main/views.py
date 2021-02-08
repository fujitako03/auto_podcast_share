
from flask import redirect, render_template, request, url_for

from main import app, db
from main.models import Broadcast, Podcast


@app.route('/')
def show_podcasts():
    podcasts = Podcast.query.all()
    broadcasts = Broadcast.query.all()
    print(podcasts)
    print(broadcasts)
    return render_template('podcasts.html',podcasts=podcasts, broadcasts=broadcasts)


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
