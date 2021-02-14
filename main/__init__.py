from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# アプリを宣言
app = Flask(__name__)
app.config.from_object('main.config')

# dbを設定
db = SQLAlchemy(app) 
import init_db

import main.views
