from flask import Flask
from flask_restful import Api

from app.models import db
from app.resources.auth import UserRegister, UserLogin
from app.resources.bucketlist import BucketList, BucketLists, FetchBucketList, BucketListEdit 
from app.resources.item import BucketListItem,  EditBucketListItem




app = Flask(__name__)
api = Api(app)

api.add_resource(UserRegister, '/v1/auth/register')
api.add_resource(UserLogin, '/v1/auth/login')
api.add_resource(FetchBucketList, '/v1/bucketlists/<int:id>')
api.add_resource(BucketList, '/v1/bucketlist')
api.add_resource(BucketLists,'/v1/bucketlists ')
api.add_resource(BucketListEdit, '/v1/bucketlists/<int:id>')
api.add_resource(BucketListItem, '/v1/bucketlists/<int:id>/item')
api.add_resource(EditBucketListItem, '/v1/bucketlists/<int:bucket_id>/item/<int:item_id>')



if __name__ == '__main__':
    app.run(debug=True)