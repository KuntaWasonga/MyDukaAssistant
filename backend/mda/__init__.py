from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

#instantiate the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config['SECRET_KEY'] = '865056bk9e4a5162b711a9a0a967a791'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myda.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager(app)

from mda import routes
