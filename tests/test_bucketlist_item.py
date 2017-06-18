import unittest
import json

import run

from app.models import db


class TestBucketlistItems(unittest.TestCase):

    def setUp(self):

        self.client = run.app.test_client()
        db.create_all()
        user = {"username": "rozzah", "password": "password"}
        userdata = json.dumps(user)
        self.client.post(
            "/v1/auth/register", data=userdata, content_type="application/json")

        response = self.client.post(
            "/v1/auth/login", data=userdata, content_type="application/json")
        self.token = json.loads(response.data.decode())['Authorization']
        self.headers = {'Content-Type': 'application/json',
                         'Authorization': self.token}
        bucket_list = {"name": "interior_design"}
        self.client.post(
            "/v1/bucketlists", data=json.dumps(bucket_list), headers=self.headers)

    def tearDown(self):
        db.drop_all()

    def test_create_bucketlist_item_fails_if_user_not_loged_in(self):
        """
        Test token based authentication,
        A user cannot create bucketlists items without loging in
        """
        bucketlist_item = {"name": "home interior design"}
        response = self.client.post(
            "/v1/bucketlists/1/item", data=json.dumps(bucketlist_item), headers=None)
        self.assertEqual(response.status_code, 401)

    def test_create_bucketlist_items(self):
        """Test a user can create bucketlist items """
        bucketlist_item = {"name": "home interior design"}
        response = self.client.post(
            "/v1/bucketlists/1/item", data=json.dumps(bucketlist_item), headers=self.headers)
        print(response)
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode())

        self.assertEqual(output['message'],
                         "Bucket item created successfully.")

    def test_update_bucketlist_item(self):
        """ITEM EDIT"""
        bucketlist_item = {"name": "home interior design"}
        response = self.client.post(
            "/v1/bucketlists/1/item", data=json.dumps(bucketlist_item), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        updated_bucketlist_item = {
            "name": "home interior design by the end of june 2017"}
        response = self.client.put(
            "/v1/bucketlists/1/item/1", data=json.dumps(updated_bucketlist_item), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode())
        self.assertEqual(output['message'],
                         "You have edited the bucketlist")

    def test_delete_bucketlist_item(self):
        bucketlist_item = {"name": "home interior design"}
        response = self.client.post(
            "/v1/bucketlists/1/item", data=json.dumps(bucketlist_item), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        response = self.client.delete(
            "/v1/bucketlists/1/item/1", data=json.dumps(bucketlist_item), headers=self.headers)
        self.assertEqual(response.status_code, 204)
        print(response)
        