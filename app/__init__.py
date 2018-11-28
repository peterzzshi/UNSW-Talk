from flask import Flask
from config import Config

from pymongo import MongoClient
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient('localhost', 27017)
db = client["UNSW-Talk"]
migrate = Migrate(app, db)
login = LoginManager(app)



from app import routes