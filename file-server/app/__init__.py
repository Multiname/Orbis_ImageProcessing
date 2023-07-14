from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import os
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")
app.config["UPLOAD_FOLDER"] = config.BaseConfig.UPLOAD_FOLDER
if not os.path.exists(os.getcwd() + app.config["UPLOAD_FOLDER"]):
    os.mkdir(os.getcwd() + app.config["UPLOAD_FOLDER"])
app.json.sort_keys = config.BaseConfig.JSON_SORT_KEYS
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

engine = create_engine("postgresql://postgres:2458173671@postgres:5432/file_server")
if not database_exists(engine.url):
    create_database(engine.url)

from . import api
