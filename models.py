from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Writer(db.Model):
    __tablename__ = 'writers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    years = db.Column(db.String(50))
    era = db.Column(db.String(20))
    photo = db.Column(db.String(200))
    bio = db.Column(db.Text)
    books = db.relationship('Book', backref='writer', lazy=True)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    plot = db.Column(db.Text)
    cover = db.Column(db.String(200))
    views = db.Column(db.Integer, default=0)
    writer_id = db.Column(db.Integer, db.ForeignKey('writers.id'), nullable=False)
    quotes = db.relationship('Quote', backref='book', lazy=True)

class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(100))
    likes = db.Column(db.Integer, default=0)
    writer_id = db.Column(db.Integer, db.ForeignKey('writers.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Shelf(db.Model):
    __tablename__ = 'shelves'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    status = db.Column(db.String(20), default='read')