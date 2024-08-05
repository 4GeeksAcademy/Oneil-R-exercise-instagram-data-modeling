import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)

    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    followers = relationship('Follower', foreign_keys='Follower.user_to_id')
    following = relationship('Follower', foreign_keys='Follower.user_from_id')

class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)

    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

class Comment(Base):
    __tablename__ = 'Comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)

    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Follower(Base):
    __tablename__ = 'Follower'
    user_from_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('User.id'), primary_key=True)

class Media(Base):
    __tablename__ = 'Media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_types'), nullable=False)
    url = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)

    post = relationship('Post', back_populates='media')

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')  # Save the file in the current directory
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
