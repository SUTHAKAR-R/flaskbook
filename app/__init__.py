from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config


db = SQLAlchemy()  # For Database

bcrypt = Bcrypt()  # For password hashing

login_manager = LoginManager()  # For User login session .Go to models to setup current_user

login_manager.login_view = 'users.login'  # For @login_required

login_manager.login_message_category = 'info' # Class for messages from flask_login

mail = Mail()




def create_app(config_class=Config):

	# Construct the core app object
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app) 
	login_manager.init_app(app)
	mail.init_app(app)


	# Routes Integration
	from app.main.routes import main
	from app.users.routes import users
	from app.posts.routes import posts
	from app.errors.handlers import errors

	app.register_blueprint(main)
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(errors)

	return app