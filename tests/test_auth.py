import unittest
import json
import run

from app.models import db


class TestUserAuthentication(unittest.TestCase):

    def setUp(self):
        """Initialises the tests"""
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

    def test_register_user(self):
        """test if a user is successfully created """
        user = {"username": "rozzah1", "password": "password"}
        userdata = json.dumps(user)
        response = self.client.post(
            "/v1/auth/register", data=userdata,
            content_type="application/json")
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data)
        self.assertEqual(output['message'], "User created successfully")

    def test_register_user_already_exist(self):
        """Test a user exist """

        user = {"username": "rozzah", "password": "password"}
        userdata = json.dumps(user)
        self.client.post(
            "/v1/auth/register", data=userdata,
            content_type='application/json')
        response = self.client.post(
            "/v1/auth/register", data=userdata,
            content_type='application/json')
        self.assertEqual(response.status_code, 409)
        output = json.loads(response.data.decode())
        self.assertEqual(output['error'], "User already exist")

    def test_login_user(self):
        """Test user can login """
        user = {"username": "rozzah", "password": "password"}
        userdata = json.dumps(user)
        response = self.client.post(
            "/v1/auth/login", data=userdata, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode())
        self.assertEqual(output['message'],
                         "You have been logged in successfully")

    def test_login_user_with_invalid_credentials(self):
        """Test a user cannot login in with invalid credentials"""
        user = user = {"username": "bush", "password": "1234"}
        userdata = json.dumps(user)
        response = self.client.post(
            "/v1/auth/login", data=userdata, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data.decode())
        self.assertEqual(output['error'], "Invalid username/password")

    def tearDown(Self):
        db.drop_all()
