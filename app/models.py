from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from datetime import datetime

from app import db, login_manager

from flask import current_app

from flask_login import UserMixin

""" The user_loader call back is to tell the flask-login extension where to look for the 
        user and how to load it from the (stored in the) database/session using unique 'user_id' key """


# Setting up current_user for user login session.

# Flask-Login keeps track of the logged in user by storing its unique identifier in Flask's user session,
# a storage space assigned to each user who connects to the application.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    #current_user = User.query.get(int(user_id))


"""The User model also needs to implement four methods which can be imported from UserMixin"""
# is_authenticated: a property that is True if the user has valid credentials or False otherwise.
# is_active: a property that is True if the user's account is active or False otherwise.
# is_anonymous: a property that is False for regular users, and True for a special, anonymous user.
# get_id(): a method that returns a unique identifier for the user as a string.


class User(db.Model, UserMixin):

    # __tablename__ = 'user' default table name can be overridden.

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self,expires_in=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        

    def __repr__(self):
        return f"<User: {self.username}, {self.email}, {self.image_file}>"


class Post(db.Model):

    # __tablename__ = 'post' default table name can be overridden.

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Post: {self.title}, {self.date_posted}>"
