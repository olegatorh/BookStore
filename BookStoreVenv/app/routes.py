from app import app, db
from flask import render_template, request, url_for, redirect, flash
from werkzeug.urls import url_parse
from app.models import Posts, User, Comments, CartAndWish
from flask_login import current_user, login_user
from app.forms import LoginForm, RegistrationForm, BookStoreForm
from flask_login import logout_user, login_required


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    page = request.args.get('page', 1, type=int)

    # кількісь постів на головній сторінці (міняється в конфігу)
    PostsPerPage = Posts.query.order_by(Posts.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=PostsPerPage.next_num) if PostsPerPage.has_next else None
    prev_url = url_for('index', page=PostsPerPage.prev_num) if PostsPerPage.has_prev else None
    return render_template('index.html', title='BuySomeMusic', posts=PostsPerPage.items, prev_url=prev_url,
                           next_url=next_url, page=page)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sing In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        if user.username == type(int):
            flash('Invalid username')
            return redirect(url_for('register'))
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/<bookName>', methods=["GET", "POST"])
def bookPage(bookName):
    posts = Posts.query.filter_by(bookName=bookName).first()
    user = User.query.all()
    form = BookStoreForm()
    comments = Comments.query.all()
    comments.reverse()
    if 'cart' in request.form:
        if current_user.is_authenticated:
            cartandwish = CartAndWish(cart=bookName, username=current_user.username)
            db.session.add(cartandwish)
            db.session.commit()
            return redirect(f"http://192.168.1.15:9000/{bookName}")
        else:
            return redirect(url_for("login"))
    elif 'wish_list' in request.form:
        if current_user.is_authenticated:
            cartandwish = CartAndWish(wish_list=bookName, username=current_user.username)
            db.session.add(cartandwish)
            db.session.commit()
            return redirect(f"http://192.168.1.15:9000/{bookName}")
        else:
            return redirect(url_for("login"))

    if "submit" in request.form and len(form.body.data) >= 1:
        comment = Comments(body=form.body.data, user_name=current_user.username, book_id=bookName)
        db.session.add(comment)
        db.session.commit()
        flash("your comment is live now!")
        return redirect(f"http://192.168.1.15:9000/{bookName}")


    return render_template('bookPage.html', title=bookName, posts=posts,
                           form=form, comments=comments, bookName=bookName, user=user)


@app.route('/cart', methods=["GET", "POST"])
@login_required
def cart():
    return render_template("cart.html", title="Cart")


@app.route('/wishlist', methods=["GET", "POST"])
@login_required
def wishlist():
    cartandwish = CartAndWish.query.all()
    return render_template("wishlist.html", title="Wish List", cartandwish=cartandwish)


@app.route('/myBooks', methods=["GET", "POST"])
@login_required
def myBooks():
    return render_template("myBooks.html", title="My Books")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



