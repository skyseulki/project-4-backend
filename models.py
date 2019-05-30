import datetime

from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin


DATABASE = SqliteDatabase('posts.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where(
                (cls.email==email)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            raise Exception('Email is already in use')
            # return 'User with that email already exists'

class Post(Model):
    name = CharField()
    address = CharField()
    cuisine = CharField()
    picture = CharField()
    review = CharField()
    cost = CharField()
    # created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class CommentRev(Model):
    comments = CharField()
    username = CharField()
    userId = ForeignKeyField(User, related_name='commentrevs')
    postId = ForeignKeyField(Post, related_name='commentPost')

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, CommentRev], safe=True)
    DATABASE.close()
