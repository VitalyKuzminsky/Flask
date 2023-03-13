from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from blog.app import db
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Имя таблицы

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    password = Column(String(255))

    author = relationship('Author', uselist=False, back_populates='user')

    # username = Column(String(80), unique=True, nullable=False)
    # is_staff = Column(Boolean, nullable=False, default=False)

    # def __repr__(self):
    #     return f"<User #{self.id} {self.username!r}>"

    # def check_password(self, password: str) -> bool:
    #     return check_password_hash(self.password, password)


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='author')
    articles = relationship('Article', back_populates='author')


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('authors.id'), nullable=False)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship('Author', back_populates='articles')


# Преподаватель забил на это всё дело, сказал, что пришлёт код, но мы же видео смотрим =(
# class Article(db.Model):
#     __tablename__ = 'articles'
#
#     title = Column(String(255))
#     text = Column(String)
#     author = relationship('User')  # Один ко многим
