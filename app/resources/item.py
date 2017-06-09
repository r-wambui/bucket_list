from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource, Api, fields, reqparse
from flask import g, request, Flask

from app.models import db, UserModel, BucketlistItem, Bucketlist

auth = HTTPTokenAuth(scheme="Token")


@auth.verify_token
def verify_token(token):
    """To validate the token sent by the user."""
    user = UserModel.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

parser = reqparse.RequestParser()
parser.add_argument(
    'name', required=True, help='Please enter the item names'
)
parser.add_argument(
    'done', type=str, help='Limit must be a number',

)


class BucketListItem(Resource):
    @auth.login_required
    def post(self, id):
        args = parser.parse_args()
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            return (
                {"error": "There is no bucketlist with the given id."},
                404)

        bucketlist_item = BucketlistItem.query.filter_by(
            name=args.name, bucketlist_id=bucketlist.id).first()
        if bucketlist_item:
            return {"error": "An item with the name exist."}, 409

        else:
            item = BucketlistItem(name=args.name, done=False, created_by=g.user.id,
                                  bucketlist_id=bucketlist.id)

            db.session.add(item)
            db.session.commit()

            return {"message": "Bucket item created successfully."}, 201


class EditBucketListItem(Resource):
    @auth.login_required
    def put(self, bucket_id, item_id,):
        args = parser.parse_args()
        bucketlist = Bucketlist.query.filter_by(id=bucket_id).first()

        if not bucketlist:
            return (
                {"error": "This no bucketlist with the given id."},
                404)
        item = BucketlistItem.query.filter_by(id=item_id).first()
        if not item:
            return ({"error": "No item with the given id."}, 404)
        if args.name:
            if item.created_by == g.user.id:

                if BucketlistItem.query.filter_by(name=args.name.lower(), bucketlist_id=bucket_id).first():
                    return ({"error": "You can not edit with the same name."}, 409)
                else:
                    item.name = args.name
                    db.session.add(item)
                    db.session.commit()
                    return ({
                        "name": args.name,
                        'message': 'You have edited the bucketlist'
                    }), 201
            else:
                return ({"error": "You can only edit your own bucket lists."}, 401)

    @auth.login_required
    def delete(self, bucket_id, item_id):
        bucketlist = Bucketlist.query.filter_by(id=bucket_id).first()

        if not bucketlist:
            return (
                {"error": "There is no bucketlist with the given id."},
                404)
        item = BucketlistItem.query.filter_by(
            id=item_id, bucketlist_id=bucket_id).first()
        if not item:
            return ({"error": "The bucketlist has no Item with the given id."}, 404)

        if item.created_by == g.user.id:
            db.session.delete(item)
            db.session.commit()
            return ({"message": "delete successful"}, 204)
        elif item.created_by != g.user.id:
            return ({"error": "You can only delete your own buckelist."}, 401)
