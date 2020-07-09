from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookName = db.Column(db.String(64), index=True, unique=True)
    author = db.Column(db.String(64))
    BookImgLink = db.Column(db.String(128))
    cost = db.Column(db.String(32))
    description = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    lenght = db.Column(db.Integer)
    language = db.Column(db.String(64))
    rating = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'book id: {self.id}, name: {self.bookName}, amount: {self.amount},' \
               f' cost: {self.cost}, timePost: {self.timestamp}>'

    def mainDesc(self):
        """функція для переробки опису під карту на головній сторінці"""
        mainDescription = self.description[:56].rstrip() + '...'
        return mainDescription


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cart = db.Column(db.String(100))
    wish_list = db.Column(db.String(100))

    def __repr__(self):
        return f"id:{self.id}, username:{self.username}, email:{self.email}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    book_id = db.Column(db.String)
    user_name = db.Column(db.String)

    def __repr__(self):
        return f"Book_id: {self.book_id}, User Name: {self.user_name}, timestamp: {self.timestamp} "


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
