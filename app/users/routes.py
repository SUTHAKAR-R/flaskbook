from flask import render_template, flash, redirect, url_for, request, Blueprint

from app.users.forms import SignupForm, LoginForm, UpdateAccountForm, RequestPasswordResetForm, PasswordResetForm

from flask_login import login_required, login_user, logout_user, current_user

from app import db, bcrypt

from app.models import User, Post

from app.users.utils import save_picture, send_reset_mail

users = Blueprint('users',__name__)

@users.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data,email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Account Created.Login to explore!', 'success')
		return redirect(url_for('users.login'))

	return render_template('signup.html', title='Signup', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():

		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			flash(f'Logged in successfully. Have fun {user.username}!', 'success')

			next_page = request.args.get('next')
			return redirect(next_page) if next_page else  redirect(url_for('main.home'))
		else:
			flash(f'Login unsuccessful.Please check your email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
	logout_user()
	flash(f'Logged out successfully!','success')
	return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()

	#During GET method if won't be executed.
	if form.validate_on_submit():
		if form.picture.data:
			current_user.image_file = save_picture(form.picture.data)
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Changes made!','success')
		form.username.data = current_user.username 
		form.email.data = current_user.email
		return redirect(url_for('users.account'))

	#During GET method elif will be executed.
	elif request.method == 'GET':
		form.username.data = current_user.username 
		form.email.data = current_user.email

	image_file = url_for('static',filename=f'profile_pics/{current_user.image_file}')
	return render_template('account.html',title='Account',image_file_path=image_file, form=form)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestPasswordResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_mail(user)
		flash('A password reset verification link has been sent your email.Please verify your mail', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html',title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	user = User.verify_reset_token(token)
	if user is None:
		flash('The link is invalid or expired','warning')
		return redirect(url_for('users.password_reset_request'))
	form = PasswordResetForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f'Your password has been changed', 'success')
		return redirect(url_for('users.login'))

	return render_template('reset_password.html', title='Reset Password', form=form)
