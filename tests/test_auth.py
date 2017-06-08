import unittest
import json
import run


class TestUserAuthentication(unittest.TestCase):

    def setUp(self):
        self.client = run.app.test_client()

    def test_user_registration(self):
        """test if a user is successfully created """
        user = {"username": "rozzah", "password": "password"}
        userdata = json.dumps(user)
        response = self.client.post(
            "/v1/auth/register", data=userdata, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data)
        self.assertEqual(output['message'], "User created successfully")

    def test_user_registration_user_already_exist(self):
        """Test a user exist """
        user = {"username": "rozzah", "password": "password"}
        userdata = json.dumps(user)
        response = self.client.post(
            "/v1/auth/register", data=userdata, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        output = json.loads(response.data.decode())
        self.assertEqual(output['error'], "User already exist")

    def test_user_login(self):
        """Test user can login """
        user = {"username": "rozzah", "password": "password"}
        userdata = json.dumps(user)
        response = self.client.post(
            "/v1/auth/login", data=userdata, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode())
        self.assertEqual(output['message'],
                         "You have been loged in successfully")

    def test_user_cannot_login_with_invalid_credentials(self):
        """Test a user cannot login in with invalid credentials"""
        user = user = {"username": "bush", "password": "1234"}
        userdata = json.dumps(user)
        response = self.client.post(
            "/v1/auth/login", data=userdata, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data.decode())
        self.assertEqual(output['error'], "Invalid username/password")
