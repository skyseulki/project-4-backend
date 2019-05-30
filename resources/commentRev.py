from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)

import models

commentRev_fields = {
    'id' : fields.Integer,
    'comments': fields.String,
    'userId': fields.String,
    'postId': fields.String,
    'username': fields.String
}

class CommentPost(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument(
            'comments',
            required=False,
            help='No title provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'userId',
            required=False,
            help='No title provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'postId',
            required=False,
            help='No title provided',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'username',
            required=False,
            help='No title provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        comments = [marshal(comment, commentRev_fields) for comment in models.CommentRev.select()]
        return comments

    @marshal_with(commentRev_fields)
    def post(self):
        args = self.reqparse.parse_args()
        comment = models.CommentRev.create(**args)
        return comment


comment_api = Blueprint('resources.commentRev', __name__)
api = Api(comment_api)
api.add_resource(
    CommentPost,
    '/comment'
)
