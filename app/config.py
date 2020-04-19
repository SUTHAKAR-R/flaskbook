from os import environ

class Config:

	# General config
	SECRET_KEY = environ.get('SECRET_KEY')

	# Database config
	SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Mail config
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = environ.get('MAIL_PASSWORD')