from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS

#instantiate the app
app = Flask(__name__)
CORS(app, supports_credentials=True)

#-----------------DATABASE CONFIGURATIONS----------------------------#
app.config['SECRET_KEY'] = '865056bk9e4a5162b711a9a0a967a791'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myda.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

migrate = Migrate(app, db)


#--------------------LOGIN CONFIGURATION-----------------------------#

login_manager = LoginManager(app)


#---------------------BLUEPRINT IMPORTS--------------------------------#
from .routes.shopper_routes import shopper_bp
app.register_blueprint(shopper_bp)

from .routes.employee_routes import employee_bp
app.register_blueprint(employee_bp)

from .routes.product_routes import product_bp
app.register_blueprint(product_bp)

from .routes.cart_routes import cart_bp
app.register_blueprint(cart_bp)
