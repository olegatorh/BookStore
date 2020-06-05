from app import app, db
from flask import render_template, request, url_for
from app.models import Posts

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    page = request.args.get('page', 1, type=int)
    # кількісь постів на головній сторінці (міняється в конфігу)
    PostsPerPage = Posts.query.order_by(Posts.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=PostsPerPage.next_num) if PostsPerPage.has_next else None
    prev_url = url_for('index', page=PostsPerPage.prev_num) if PostsPerPage.has_prev else None
    return render_template('index.html', title='BuySomeMusic', posts=PostsPerPage.items, prev_url=prev_url, next_url=next_url, page=page)


@app.route('/<bookName>', methods=["GET", "POST"])
def bookPage(bookName):
    posts = Posts.query.filter_by(bookName=bookName).first()

    return render_template('bookPage.html', title=bookName, posts=posts)

