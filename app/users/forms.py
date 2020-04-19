from flask_wtf import FlaskForm

from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, SubmitField, BooleanField

from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from flask_login import current_user

from app.models import User

class SignupForm(FlaskForm):

	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])

	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')

	"""WTForms (in the definition of validate())is checking for extra functions defined with the naming pattern
		'validate_(field name)' and later calling those extra functions 
		and implicitly executes them without being called"""

	"""When you add any methods that match the pattern validate_<field_name>,
	   WTForms takes those as custom validators and implicitly invokes them in addition to the stock validators"""

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		#checking if the user is in the database upfront.
		if user:
			raise ValidationError('Username is already taken.Please choose a different one.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This email is already registered.Please try logging in.')


class LoginForm(FlaskForm):

	email = StringField('Email', validators=[DataRequired(), Email()])

	password = PasswordField('Password', validators=[DataRequired()])

	remember = BooleanField('Remember Me')

	submit = SubmitField('Login')


#In user login session
class UpdateAccountForm(FlaskForm):

	#Fields that are passed to the html to get rendered.
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

	email = StringField('Email', validators=[DataRequired(), Email()])

	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

	submit = SubmitField('Make Changes')

	#These functions are implicitly called by the flaskform and rendered as conditions/validators to the fields. 
	#These functions run upfront while making changes.

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username is taken.Please choose a different one.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email is taken.Try logging in.')


class RequestPasswordResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	
	submit = SubmitField('Request Password Reset')

class PasswordResetForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Reset Password')
	