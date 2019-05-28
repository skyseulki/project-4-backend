import json

from flask import jsonify, Blueprint, abort, make_response
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)
from flask_login import login_user, logout_user, login_required, current_user

import models

user_fields = {
    'username': fields.String,
}

class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=False,
            help='username does not exist',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=False,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=False,
            help='No password verification provided',
            location=['form', 'json']
        )
        super().__init__()
    
    def get(self):
        return jsonify({'users': [{'username': 'Franklin'}]})

    def post(self):
        args = self.reqparse.parse_args()
        if args['password'] == args['verify_password']:
            print(args, '<------ args (req.body)')
            user = models.User.create_user(**args)
            login_user(user)
            return marshal(user, user_fields), 201
        return make_response(
            json.dumps({
                'error': 'Password verification incorrect. Try Again.'
            }), 400)


class User(Resource):
    def get(self, id):
        return jsonify({'username': 'Franklin'})
    
    def put(self, id):
        return jsonify({'username': 'Franklin'})

    def delete(self, id):
        return jsonify({'username': 'Franklin'})




users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/registration'
)

