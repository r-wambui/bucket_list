from flask import Flask
from flask_restful import Api

from app.models import db
from app.resources.auth import UserRegister, UserLogin
from app.resources.bucketlist import BucketList, BucketListEdit 



app = Flask(__name__)
api = Api(app)

api.add_resource(UserRegister, '/v1/auth/register')
api.add_resource(UserLogin, '/v1/auth/login')
api.add_resource(BucketList, '/v1/bucketlists')
api.add_resource(BucketListEdit, '/v1/bucketlists/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)