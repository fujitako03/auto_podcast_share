import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# アプリを宣言
app = Flask(__name__)
app.config.from_object('config.config')

# dbを設定
db = SQLAlchemy(app) 
from main.models.init_db import init_db

logging.info("start init db")
init_db()
logging.info("finish init db")


import main.views
