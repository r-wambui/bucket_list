from urllib.parse import urljoin

from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource, reqparse
from flask import g, request, Flask, url_for

from app.models import db, Bucketlist, User


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

auth = HTTPTokenAuth(scheme="Token")


@auth.verify_token
def verify_token(token):
    """To validate the token sent by the user."""
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


parser = reqparse.RequestParser()
parser.add_argument(
    'name', required=True, help='Please enter a bucketlist name'
)
parser.add_argument(
    'limit', type=int, help='Limit must be a number',
    required=False
)
parser.add_argument(
    'q', type=str, help='Query must be a string',
    required=False
)
parser.add_argument(
    "page", type=int, required=False, )


class CreateBucketList(Resource):
    """Create a bucketlist,
         A user must login
    """

    @auth.login_required
    def post(self):
        args = parser.parse_args()
        bucketlist = Bucketlist.query.filter_by(
            name=args.name, created_by=g.user.id).first()

        if bucketlist:
            return "You already have a bucketlist with that name", 409

        bucketlist = Bucketlist(name=args.name, created_by=g.user.id)
        db.session.add(bucketlist)
        db.session.commit()

        return ({
            "name": args.name,
            'message': 'You have created a new bucket list'}), 201


class SingleBucketList(Resource):
    """ Fetching a single bucketlist by ID"""
    @auth.login_required
    def get(self, id):
        # fetch bucketlist by id
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if bucketlist:
            if bucketlist.created_by == g.user.id:
                return {"id": bucketlist.id,
                        "name": bucketlist.name,

                        "items": [{
                            "id": item.id,
                            "name": item.name,
                            "date_created": str(item.date_created),
                            "date_modified": str(item.date_modified),
                            "done": item.done}
                            for item in bucketlist.bucketitems],
                        "date_created": str(bucketlist.date_created),
                        "date_modified": str(bucketlist.date_modified),
                        "created_by": bucketlist.created_by, }

        else:
            return (
                {"error": "There is no bucketlist with the given id."},
                404)


class AllBucketList(Resource):
    """Fetch all users bucketlists,
        with pages and limit of the bucketlists
    """
    @auth.login_required
    def get(self):
        page = request.args.get('page')
        limit = request.args.get('limit')
        q = request.args.get('q')

        # Search bucketlist by the name
        if q:
            bucketlists = (Bucketlist.query.filter(
                Bucketlist.name.like('%{}%'.format(
                    q.lower()))).filter_by(
                created_by=int(str(g.user.id))).all())

            if bucketlists:
                search = []
                for bucketlist in bucketlists:
                    search.append({"id": bucketlist.id,
                                   "name": bucketlist.name,
                                   "items": [{
                                       "id": item.id,
                                       "name": item.name,
                                       "date_created":
                                       str(item.date_created),
                                       "date_modified":
                                       str(item.date_modified),
                                       "done": item.done}
                                       for item in bucketlist.bucketitems],
                                   "date_created":
                                   str(bucketlist.date_created),
                                   "date_modified":
                                   str(bucketlist.date_modified),
                                   "created_by": bucketlist.created_by, })

                return search, 200
            else:
                return ({"error":
                         "You have no bucketlist with the name."},
                        404)
        # get all bucketlists with pages and limit
        if page and limit:
            bucketlists = (Bucketlist.query.filter_by(
                created_by=g.user.id).paginate(page=int(page),
                                               per_page=int(limit),
                                               error_out=False))

            buckets, next_url, prev_url = [], None, None

            if bucketlists:
                for bucketlist in bucketlists.items:

                    buckets.append({"id": bucketlist.id,
                                    "name": bucketlist.name,
                                    "items": [{
                                        "id": item.id,
                                        "name": item.name,
                                        "date_created":
                                        str(item.date_created),
                                        "date_modified":
                                        str(item.date_modified),
                                        "done": item.done}
                                        for item in bucketlist.bucketitems],
                                    "date_created":
                                    str(bucketlist.date_created),
                                    "date_modified":
                                    str(bucketlist.date_modified),
                                    "created_by": bucketlist.created_by, })
                    # checking the next page
                if bucketlists.has_next:
                    next_url = urljoin("http://127.0.0.1:5000/",
                                       "/v1/bucketlists"), url_for(
                        "allbucketlist",
                        page=bucketlists.next_num,
                        limit=bucketlists.per_page)
                # checking th eprevious page
                if bucketlists.has_prev:
                    prev_url = (urljoin("http://127.0.0.1:5000/",
                                        "/v1/bucketlists"), url_for(
                        "allbucketlist",
                        page=bucketlists.prev_num,
                        limit=bucketlists.per_page))

                if buckets:
                    page_details = {
                        "start": bucketlists.page,
                        "limit": limit,
                        "next_page": next_url,
                        "prev_page": prev_url,
                        "bucketlists": buckets
                    }
                    return page_details, 200
                else:
                    return {"error":
                            "You have no bucketlists on that page"}, 404
        else:
            bucketlists = (Bucketlist.query.filter_by(
                created_by=g.user.id))
            # create an empty list that will store the bucketlists
            buckets = []
            if bucketlists:
                for bucketlist in bucketlists:

                    buckets.append({"id": bucketlist.id,
                                    "name": bucketlist.name,
                                    "items": [{
                                        "id": item.id,
                                        "name": item.name,
                                        "date_created": str(item.date_created),
                                        "date_modified":
                                        str(item.date_modified),
                                        "done": item.done}
                                        for item in bucketlist.bucketitems],
                                    "date_created":
                                    str(bucketlist.date_created),
                                    "date_modified":
                                    str(bucketlist.date_modified),
                                    "created_by": bucketlist.created_by, })
                return buckets, 200
            else:
                return {"error": "You have no bucketlists"}, 404


class BucketListEdit(Resource):
    """Edit and delete the bucketlist by the given ID"""
    @auth.login_required
    def put(self, id):
        args = parser.parse_args()
        bucketlist = Bucketlist.query.filter_by(id=id).first()

        if not bucketlist:
            return ({"error": "No bucketlist with the given id."}, 404)

        if args.name:
            if bucketlist.created_by == g.user.id:

                if Bucketlist.query.filter_by(name=args.name.lower()).first():
                    return ({"error":
                             "You can not edit with the same name."}, 409)

                bucketlist.name = args.name
                db.session.add(bucketlist)
                db.session.commit()
                return ({
                    "name": args.name,
                    'message': 'You have updated the bucketlist'
                }), 201
            else:
                return ({"error": "Invalid ID."}, 403)

    @auth.login_required
    def delete(self, id):
        bucketlist = Bucketlist.query.filter_by(id=id).first()

        if bucketlist:
            if bucketlist.created_by == g.user.id:
                db.session.delete(bucketlist)
                db.session.commit()
                return ({"message": "delete successful"}, 204)

            elif bucketlist.created_by != g.user.id:
                return ({"error": "Invalid ID."}, 403)
        else:
            return ({"error": "bucketlist does not exist."}, 404)
