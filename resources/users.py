import json

from flask import jsonify, Blueprint, abort, make_response
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
import models

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
}

class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email Provided',
            location=['form', 'json']
        )
        super().__init__()

    # def get(self):
    #     return jsonify({'users': [{'username': 'Franklin'}]})

    def get(self):
        posts = [marshal(user, user_fields) for user in models.User.select()]
        return posts

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
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        try:
            args = self.reqparse.parse_args()
            user = models.User.get(models.User.username==args['username'])
            if(user):
                if(check_password_hash(user.password, args['password'])):
                    return make_response(
                        json.dumps({
                            'user': marshal(user, user_fields),
                            'success': True
                        }), 200)

                else:
                    return make_response(
                        json.dumps({
                            'message': 'incorrect password'
                        }), 401)
        except models.User.DoesNotExist:
            return make_response(
                json.dumps({
                    'message': 'Username does not exist'
                }), 400)


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

api.add_resource(
    User,
    '/login'
)


#just to commit
