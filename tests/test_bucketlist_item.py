import unittest
import json

import run


class TestBucketlistItems(unittest.TestCase):

    def setUp(self):

        self.client = run.app.test_client()
        user = {"username": "rozzah", "password": "password"}
        userdata = json.dumps(user)
        response = self.client.post("/v1/auth/login", data=userdata)
        access_token = ['access_token']
        self.headers = {'Authorization': access_token}

    def tearDown(self):
        pass

    def test_create_bucketlist_item_fails_if_user_not_loged_in(self):
        """
        Test token based authentication,
        A user cannot create bucketlists items without loging in
        """
        bucketlist_item = {"name": "home interior design"}
        response = self.client.post(
            "api/v1/bucketlists/1/items", data=json.dumps(bucketlist_item), headers=None)
        self.assertEqual(response.status_code, 401)

    def test_create_bucketlist_items(self):
        """Test a user can create bucketlist items """
        bucketlist_item = {"name": "home interior design"}
        response = self.client.post(
            "/v1/bucketlists/1/items", data=json.dumps(bucketlist_item), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode())
        self.assertEqual(output['message'],
                         "You have created a new bucketlist item")

    def test_update_bucketlist_item(self):
        """ITEM EDIT"""
        bucketlist_item = {"name": "home interior design"}
        response = self.client.post(
            "api/v1/bucketlists/1/items", data=json.dumps(bucketlist_item), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        updated_bucketlist_item = {
            "name": "home interior design by the end of june 2017"}
        response = self.client.put(
            "/v1/bucket_lists/1/items", data=json.dumps(updated_bucketlist_item), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode())
        self.assertEqual(output['message'],
                         "You have updated the bucketlist item successfully")

    def test_delete_bucketlist_item(self):
        bucketlist_item = {"name": "home interior design"}
        response = self.client.post(
            "/v1/bucketlists/1/items", data=json.dumps(bucketlist_item), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        response = self.client.delete(
            "/v1/bucketlists/1/items", data=json.dumps(bucketlist_item), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode())
        self.assertEqual(output['message'],
                         "You have deleted the bucketlist item")
