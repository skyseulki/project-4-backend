
from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)

import models

post_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'cuisine': fields.String,
    'picture': fields.String,
    'review': fields.String,
    'cost': fields.String
}

class PostList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            'name',
            required=False,
            help='No title provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'address',
            required=False,
            help='No review provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'cuisine',
            required=False,
            help='No review provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'picture',
            required=False,
            help='No review provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'review',
            required=False,
            help='No review provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'cost',
            required=False,
            help='No review provided',
            location=['form', 'json']
        )
        super().__init__()
    
    def get(self):
        posts = [marshal(post, post_fields) for post in models.Post.select()]
        return posts
    
    @marshal_with(post_fields)
    def post(self):
        args = self.reqparse.parse_args()
        post = models.Post.create(**args)
        return post

class Post(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=False,
            help='No title provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'address',
            required=False,
            help='No review provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'cuisine',
            required=False,
            help='No review provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'picture',
            required=False,
            help='No review provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'review',
            required=False,
            help='No review provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'cost',
            required=False,
            help='No review provided',
            location=['form', 'json']
        )
        super().__init__()
    
    @marshal_with(post_fields)
    def get(self, id):
        try:
            post = (models.Post.get(models.Post.id==id), 200)
        except models.Post.DoesNotExist:
            abort (404)
        else:
            return post
    
    @marshal_with(post_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Post.update(**args).where(models.Post.id==id)
        query.execute()
        return (models.Post.get(models.Post.id==id), 200)
    
    def delete(self, id):
        query = models.Post.delete().where(models.Post.id==id)
        query.execute()
        return 'Post deleted'

posts_api = Blueprint('resources.posts', __name__)
api = Api(posts_api)

api.add_resource(
    PostList,
    '/posts'
)

api.add_resource(
    Post,
    '/posts/<int:id>'
)