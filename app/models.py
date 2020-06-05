from app import db
from datetime import datetime


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
        return f'<book id: {self.id}, name: {self.bookName}, amount: {self.amount}, cost: {self.cost}, timePost: {self.timestamp}>'

    def mainDesc(self):
        """функція для переробки опису під карту на головній сторінці"""
        mainDescription = self.description[:56].rstrip() + '...'
        return mainDescription


