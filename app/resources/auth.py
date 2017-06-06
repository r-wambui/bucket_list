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
    @marshal_with(user_fields)
    def post(self):
        args = parser.parse_args()
        user = UserModel(username=args.username, password=args.password)
        db.session.add(user)
        db.session.commit()

        return user


class UserLogin(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = parser.parse_args()
        user = UserModel(username=args.username, password=args.password)
       
        if user:
            UserModel.query.filter_by(username=args.username).first()
        else:
            return {"message": "please enter a username and password"}

        return user


