from config.config import Config

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = Config.flask.debug
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
host = Config.flask.host
