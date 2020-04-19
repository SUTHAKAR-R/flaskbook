import os

import secrets

from flask import url_for, current_app 

from app import  mail

from flask_mail import Message


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, file_extension = os.path.splitext(form_picture.filename)

	#Hashing the pictures name. We just can't save it like that.So,just for the sake of it.
	hashed_picture_filename = random_hex + file_extension
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', hashed_picture_filename)
	form_picture.save(picture_path)
	return hashed_picture_filename


def send_reset_mail(user):
	token = user.get_reset_token()
	msg = Message(subject='Password Reset Request From FlaskBook', sender='ramsuthagar09@gmail.com', recipients=[user.email])

	msg.body = f""" Click the below link to reset your password.

{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request just ignore...
	 """

	mail.send(msg)