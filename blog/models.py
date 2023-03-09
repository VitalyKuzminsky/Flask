from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
# from sqlalchemy.orm import relationship

from blog.app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Имя таблицы

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    password = Column(String(255))
    # username = Column(String(80), unique=True, nullable=False)
    # is_staff = Column(Boolean, nullable=False, default=False)

    # def __repr__(self):
    #     return f"<User #{self.id} {self.username!r}>"


# Преподаватель забил на это всё дело, сказал, что пришлёт код, но мы же видео смотрим =(
# class Article(db.Model):
#     __tablename__ = 'articles'
#
#     title = Column(String(255))
#     text = Column(String)
#     author = relationship('User')  # Один ко многим
