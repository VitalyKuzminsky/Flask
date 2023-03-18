from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash

from blog.app import db
from datetime import datetime


article_tag_associations_table = Table(
    'article_tag_association',
    db.metadata,
    db.Column('article_id', db.Integer, ForeignKey('articles.id'), nullable=False),
    db.Column('tag_id', db.Integer, ForeignKey('tags.id'), nullable=False),
)


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Имя таблицы

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    password = Column(String(255))
    is_staff = db.Column(db.Boolean, default=False)

    author = relationship('Author', uselist=False, back_populates='user')

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __str__(self):
        return f'{self.user.email} ({self.user.id})'

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

    def __str__(self):
        return self.user.email


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('authors.id'), nullable=False)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship('Author', back_populates='articles')
    tags = relationship('Tag', secondary=article_tag_associations_table, back_populates='articles')

    def __str__(self):
        return self.title


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    articles = relationship('Article', secondary=article_tag_associations_table, back_populates='tags')

    def __str__(self):
        return self.name


# Преподаватель забил на это всё дело, сказал, что пришлёт код, но мы же видео смотрим =(
# class Article(db.Model):
#     __tablename__ = 'articles'
#
#     title = Column(String(255))
#     text = Column(String)
#     author = relationship('User')  # Один ко многим
