import json

from flask_restful import Resource, Api, fields, marshal_with, reqparse

from app.models import db, UserModel


parser = reqparse.RequestParser()
parser.add_argument(
    'username', required=True,
    help='Please enter a username',
)

parser.add_argument(
    'password', type=str, required=True,
    help='Enter your password',
)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
}


class UserRegister(Resource):
    def post(self):
        args = parser.parse_args()
        person = UserModel.query.filter_by(username=args.username).first()

        if person:
            return {'error': "User already exist"}, 409

        else:
            user = UserModel(username=args.username, password=args.password)
            db.session.add(user)
            db.session.commit()    
            return {'message': 'User created successfully'}, 201



class UserLogin(Resource):
    def post(self):
        args = parser.parse_args()
        # user = UserModel(username=args.username, password=args.password)

        person = UserModel.query.filter_by(username=args.username).first()
        if person and person.verify_password(args.password):
            token = person.generate_auth_token()
            return ({'Authorization':'Token ' + token.decode('ascii'), 'message': 'You have been logged in successfully'}, 200)
        # password = UserModel.query.filter_by(password=args.password).first()
        else:
            return {'error': "Invalid username/password"}, 401




