

from flask import render_template, request, Blueprint

from app.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
	page = request.args.get(key='page', type=int, default=1)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
	return render_template('home.html', posts=posts)


@main.route('/about')
def about():
	return render_template('about.html', title='About')