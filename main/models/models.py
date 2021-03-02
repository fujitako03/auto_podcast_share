import datetime
import logging

from flask_sqlalchemy import SQLAlchemy
from main import db


class Podcast(db.Model):
    podcast_id = db.Column(db.Integer, primary_key=True)
    podcast_url = db.Column(db.String)
    podcast_name = db.Column(db.String,)

class Broadcast(db.Model):
    broadcast_id = db.Column(db.Integer,primary_key=True)
    broadcast_service = db.Column(db.String, default=0)
    broadcast_url = db.Column(db.String, default=0)
    podcast_id = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return "<Entry broadcast_id =={} broadcast_url={!r}>".format(
            self.broadcast_id, 
            self.broadcast_url,
            self.broadcast_service,
            self.podcast_id,
            self.created_at,
            self.updated_at,
            )


def init():
    logging.info("start create db")
    db.create_all()
    logging.info("finish create db")
