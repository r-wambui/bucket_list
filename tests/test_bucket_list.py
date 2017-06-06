import unittest
import json



class TestBucketList(unittest.TestCase):

    def setUp(self):

        user = {"username": "rozzah", "password": "password"}
        userdata = json.dumps(user)
        response = self.client.post("api/v1/auth/login", data=userdata)
        access_token = output['access_token']
        self.headers = {'Authorization': 'JWT' % access_token}

    def tearDown(self):
        pass

    def test_create_bucket_list_fails_if_user_not_loged_in(self):
        """
        Test token based authentication, 
        A user cannot interact without loging in
        """
        bucket_list = {"name": "interior_design"}
        response = self.client.post(
            "api/v1/bucketlists", data=json.dumps(bucket_list), headers=None)
        self.assertEqual(response.status_code, 401)

    def test_create_bucket_list(self):
        """Test a bucket_list can be created """
        bucket_list = {"name": "interior_design"}
        response = self.client.post(
            "api/v1/bucket_lists", data=json.dumps(bucket_list), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode())
        self.assertEqual(output['message'],
                         "You have created a new bucket list")

    def test_get_all_bucket_lists(self):
        """Test a user can fetch all the bucket_lists created """
        response = self.client.get("api/v1/bucket_lists", headers=self.headers)
        output = json.loads(response.data.decode())
        output = output["bucket_lists"]
        bucket_list1 = output[0]
        bucket_list2 = output[1]
        self.assertEqual(bucket_list1.get("name", "interior_design"))
        self.assertEqual(bucket_list2.get("name", "movies"))

    def test_get_single_bucket_list(self):
        """
        Test that a user can fetch a single
         bucket list using bucketlist Id
         """
        response = self.client.get(
            "api/v1/bucket_lists/1", headers=self.headers)
        output = json.loads(response.data.decode())
        self.assertEqual(output.get("name", "interior_design"))

    def test_update_bucket_list(self):
        """Test that a bucket list can be edited """
        bucket_list = {"name": "interior_design"}
        response = self.client.post(
            "api/v1/bucket_lists", data=json.dumps(bucket_list), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        updated_bucket_list = {"name": "designing"}
        response = self.client.put(
            "api/v1/bucket_lists", data=json.dumps(updated_bucket_list), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode())
        self.assertEqual(output['message'],
                         "You have updated the bucketlist successfully")

    def test_delete_bucket_list(self):
        """Test that a single bucket list can be deleted """
        bucket_list = {"name": "interior_design"}
        response = self.client.post(
            "api/v1/bucket_lists", data=json.dumps(bucket_list), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        response = self.client.delete(
            "api/v1/bucket_lists", data=json.dumps(bucket_list), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode())
        self.assertEqual(output['message'],
                         "You have deleted the bucketlist")


