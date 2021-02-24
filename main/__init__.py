from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# アプリを宣言
app = Flask(__name__)
app.config.from_object('config.config')

# dbを設定
db = SQLAlchemy(app) 
from main.models.init_db import init_db

init_db()


import main.views
