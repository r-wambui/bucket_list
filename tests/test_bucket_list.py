import unittest
import json

import run

from app.models import db


class TestBucketList(unittest.TestCase):

    def setUp(self):
        self.client = run.app.test_client()
        db.create_all()
        user = {"username": "rozzah", "password": "password"}
        userdata = json.dumps(user)
        self.client.post(
            "/v1/auth/register", data=userdata,
            content_type="application/json")

        response = self.client.post(
            "/v1/auth/login", data=userdata, content_type="application/json")
        self.token = json.loads(response.data.decode())['Authorization']
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': self.token}

    def tearDown(self):
        db.drop_all()

    def test_bucketlists_create_fails_if_user_not_logged_in(self):
        """
        Test token based authentication,
        A user cannot interact without loging in
        """
        bucket_list = {"name": "interior_design"}
        response = self.client.post(
            "/v1/bucketlists", data=json.dumps(bucket_list), headers=None)
        self.assertEqual(response.status_code, 401)

    def test_bucketlists_create(self):
        """Test a bucket_list can be created """
        bucket_list = {"name": "interior_design"}
        response = self.client.post(
            "/v1/bucketlists", data=json.dumps(bucket_list),
            headers=self.headers)
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data)
        self.assertEqual(output['message'],
                         "You have created a new bucket list")

    def test_bucketlists_get_all(self):
        """Test a user can fetch all the bucket_lists created """
        bucket_list = {"name": "interior_design"}
        bucket_list1 = {"name": "movies"}
        self.client.post(
            "/v1/bucketlists", data=json.dumps(bucket_list),
            headers=self.headers)
        self.client.post(
            "/v1/bucketlists", data=json.dumps(bucket_list1),
            headers=self.headers)
        response = self.client.get("/v1/bucketlists", headers=self.headers)

        output = json.loads(response.data)
        print(output)
        output[0] = bucket_list
        output[1] = bucket_list1
        self.assertEqual(output[0], bucket_list)
        self.assertEqual(output[1], bucket_list1)

    def test_bucketlists_fetch_one(self):
        """
        Test that a user can fetch a single
         bucket list using bucketlist Id
         """
        bucket_list = {"name": "interior_design"}
        self.client.post(
            "/v1/bucketlists", data=json.dumps(bucket_list),
            headers=self.headers)
        response = self.client.get(
            "/v1/bucketlists/1", headers=self.headers)
        output = json.loads(response.data.decode())
        self.assertEqual(output['id'], 1)

    def test_bucketlists_update(self):
        """Test that a bucket list can be edited """
        bucket_list = {"name": "interior_design"}
        response = self.client.post(
            "/v1/bucketlists", data=json.dumps(bucket_list),
            headers=self.headers)
        self.assertEqual(response.status_code, 201)
        updated_bucket_list = {"name": "designing"}
        response = self.client.put(
            "/v1/bucketlists/1", data=json.dumps(updated_bucket_list),
            headers=self.headers)
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode())
        self.assertEqual(output['message'],
                         "You have updated the bucketlist")

    def test_bucketlists_delete(self):
        """Test that a single bucket list can be deleted """
        bucket_list = {"name": "interior_design"}
        self.client.post(
            "/v1/bucketlists", data=json.dumps(bucket_list),
            headers=self.headers)
        response = self.client.delete(
            "/v1/bucketlists/1", data=json.dumps(bucket_list),
            headers=self.headers)
        self.assertEqual(response.status_code, 204)

    def test_bucketlist_delete_bucketlist_does_not_exist(self):
        bucket_list = {"name": "interior_design"}
        response = self.client.delete(
            "/v1/bucketlists/1", data=json.dumps(bucket_list),
            headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_bucketlist_update_does_not_exist(self):
        bucket_list = {"name": "interior_design"}
        response = self.client.put(
            "/v1/bucketlists/1", data=json.dumps(bucket_list),
            headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_bucketlist_search(self):
        bucket_list = {"name": "interior_design"}
        self.client.post(
            "/v1/bucketlists", data=json.dumps(bucket_list),
            headers=self.headers)
        response = self.client.get('/v1/bucketlists?q=interior_design',
                                   headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_pagination(self):
        bucket_list = {"name": "interior_design"}
        self.client.post(
            "/v1/bucketlists", data=json.dumps(bucket_list),
            headers=self.headers)
        response = self.client.get('/v1/bucketlists?page=1&limit=1',
                                   headers=self.headers)
        self.assertEqual(response.status_code, 200)

