import os
from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with, reqparse

app = Flask(__name__)
api = Api(app)


class BucketList(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=int)
        args = parser.parse_args()
        name = args["name"]
        bucketlist = BucketList(name=name)

        db.session.add(bucketlist)
        db.commit()

        return bucketlist
app.add_resource(BucketList, '/buckelist')

