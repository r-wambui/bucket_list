from urllib.parse import urljoin
import json

from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource, Api, fields, reqparse
from flask import g, request
from app.models import db, Bucketlist, UserModel

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
    'name', required=True, help='Please enter a buckeetlist name'
)
parser.add_argument(
    'limit', type=int, help='Limit must be a number',
    required=False
)
parser.add_argument(
    'query', type=str, help='Query must be a string',
    required=False
)
parser.add_argument(
    "page", type=int, required=False, )


class BucketList(Resource):

    @auth.login_required
    def post(self):
        args = parser.parse_args()
        bucketlist = Bucketlist.query.filter_by(name=args.name).first()

        if bucketlist:
            return "You already have a bucketlist with that name", 409
        else:
            # import ipdb; ipdb.set_trace()

            bucketlist = Bucketlist(name=args.name, created_by=g.user.id)
            db.session.add(bucketlist)
            db.session.commit()

            return ({
                "name": args.name,
                'message': 'You have created a new bucket list'
            }), 201

    @auth.login_required
    def get(self, id=None):
        args = parser.parse_args()
        # fetch bucketlist by id
        if id:
            bucketlist = Bucketlist.query.filter_by(id=id).first()
            if bucketlist:
                if bucketlist.created_by == g.user.id:

                    return {"id": bucketlist.id,
                            "name": bucketlist.name,
                            "date_created": str(bucketlist.date_created),
                            "date_modified": str(bucketlist.date_modified),
                            "created_by": bucketlist.created_by,
                            "items": [{
                                "id": item.id,
                                "name": item.name,
                                "done": item.done
                            }
                                for item in bucketlist.items]
                            }, 200
                else:
                    return (
                        {"error": "Bucketlist not found."},
                        404)
            # fetch all the bucket list of a user
            if args.page and args.limit:
                bucketlists = (Bucketlist.query.filter_by(
                    created_by=g.user.id).paginate(page=args.page,
                                                   per_page=args.limit))
                my_buckets = []  # create an empty bucket list
                # next_url = None
                # prev_url = None

                if bucketlists:
                    for bucketlist in bucketlists.items:
                        my_buckets.append({
                            "id": bucketlist.id,
                            "name": bucketlist.name,
                            "created_at": str(bucketlist.created_at),
                            "modified_at": str(bucketlist.modified_at),
                            "created_by": bucketlist.created_by,
                            "items": [{
                                "id": item.id,
                                "name": item.name,
                                "done": item.done
                            }
                                for item in bucketlist.items],
                        })
                    # if bucketlists.has_next:
                    #     next_url = (urljoin(
                    #         app.config["development"].BASEURL +
                    #         "/bucketlists", api.url_for(
                    #             BucketList,
                    #             page=bucketlists.next_num,
                    #             limit=bucketlists.per_page)))

                    # if bucketlists.has_prev:
                    #     prev_url = (urljoin(
                    #         configurations["development"].BASEURL +
                    #         "/bucketlists", api.url_for(
                    #             BucketList,
                    #             page=bucketlists.prev_num,
                    #             limit=bucketlists.per_page)))

                    # if my_buckets:
                    #     page_details = {
                    #         "current_page": bucketlists.page,
                    #         "limit": 2,
                    #         "next_page": next_url,
                    #         "prev_page": prev_url,
                    #         "bucketlists": my_buckets
                    #     }
                    #     return page_details, 200
                    # else:
                    #     return {"error": "You have no bucketlists"}, 404

            elif args.query:

                bucketlists = (Bucketlist.query.filter(
                    Bucketlist.name.like('%{}%'.format(
                        args['q'].lower()))).filter_by(
                    created_by=int(str(g.user.id))).all())

                if bucketlists:
                    results = []
                    for bucketlist in bucketlists:
                        results.append({
                            "id": bucketlist.id,
                            "name": bucketlist.name,
                            "created_at": str(bucketlist.created_at),
                            "modified_at": str(bucketlist.modified_at),
                            "created_by": bucketlist.created_by,
                            "items": [{
                                "id": item.id,
                                "name": item.name,
                                "done": item.done
                            }
                                for item in bucketlist.items]
                        })

                    return results, 200
                else:
                    return ({"error":
                             "You have no bucketlist containing that name."},
                            404)


class BucketListEdit(Resource):
    @auth.login_required
    def put(self, id):
        args = parser.parse_args()
        bucketlist = Bucketlist.query.filter_by(id=id).first()

        if not bucketlist:
            return ({"error": "No bucketlist with the given id."}, 404)

        if args.name:
            if bucketlist.created_by == g.user.id:

                if Bucketlist.query.filter_by(name=args["name"].lower()).first():
                    return ({"error": "You can not edit with the same name."}, 409)

                else:
                    bucketlist.name = args.name
                    db.session.add(bucketlist)
                    db.session.commit()
                    return ({
                        "name": args.name,
                        'message': 'You have edited the bucketlist'
                    }), 201
            else:
                return ({"error": "You can only edit your own bucket lists."}, 400)

    @auth.login_required
    def delete(self, id):
        bucketlist = Bucketlist.query.filter_by(id=id).first()

        if bucketlist:
            if bucketlist.created_by == g.user.id:
                db.session.delete(bucketlist)
                db.session.commit()
                return ({"message": "delete successfu"}, 204)

            elif bucketlist.created_by != g.user.id:
                return ({"error": "You can only delete your own buckelist."}, 400)
        else:
            return ({"error": "bucketlist does not exist."}, 404)
