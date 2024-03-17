import unittest
from app import app
from db_requests import *
from unittest.mock import patch
# from flask import jsonify, json
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_jwt_extended import get_jwt
from uuid import uuid4
# app.config["TESTING"] = True


class DBTestClass:

    def __init__(self, **kwargs):
        with psycopg2.connect(**kwargs) as conn:
            self.conn = conn

    def initial_connect_with_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
                            id VARCHAR(100) PRIMARY KEY,
                            email VARCHAR(30),
                            full_name VARCHAR(30),
                            password VARCHAR(200),
                            admin BOOLEAN NOT NULL
                            )""")

    def create_user(self, data):
        with self.conn.cursor() as cur:
            cur.execute(f"""INSERT INTO users 
                    ("id", "email", "full_name", "password", "admin")
                    VALUES('{data['id']}', '{data['email']}', '{data['full_name']}', '{generate_password_hash(data['password'])}', {data['admin']})""")
            cur.execute(f"""SELECT * FROM users WHERE id = '{id}'""")
            self.conn.commit()
            return cur.fetchall()

    def clean_test_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""DELETE FROM users""")
            self.conn.commit()


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db1 = DBTestClass(database="testing_db", host="localhost", user="postgres", password="postgres", port="5432")
        self.db1.initial_connect_with_db()
        uuid_patcher = patch('db_requests.uuid4')
        mock_uuid = uuid_patcher.start()
        mock_uuid.side_effect = [
            '5606bdab-ab9d-4354-a974-fbe870a54555',
        ]
        self.user_John = self.db1.create_user({"id": 'f26d75e4-3bb7-41c0-8e87-87aea01bd953',
                                              "email": 'John@john.com',
                                              "full_name": 'John',
                                              "password": 'password',
                                               "admin": False})
        self.user_Jane = self.db1.create_user({"id": '5606bdab-ab9d-4354-a974-fbe870a54101',
                                              "email": 'Jane@jane.com',
                                               "full_name": 'Jane',
                                              "password": 'password',
                                               "admin": False})

    def tearDown(self):
        db = DBTestClass(database="testing_db", host="localhost", user="postgres", password="postgres", port="5432")
        db.clean_test_db()

    def test_get_all_users(self):
        response = self.app.get('auth/user/').json
        # expected_result = [['f26d75e4-3bb7-41c0-8e87-87aea01bd953', 'John@john.com', 'John', 'password', False],
        #                    ['5606bdab-ab9d-4354-a974-fbe870a54101', 'Jane@jane.com', 'Jane', 'password', False]]
        self.assertEqual(len(response), 2)

    def test_get_user_by_id(self):
        response = self.app.get('auth/user/f26d75e4-3bb7-41c0-8e87-87aea01bd953').json
        expected_result = 'John@john.com'
        self.assertEqual(response['email'], expected_result)

    def test_get_user_by_id_not_exist(self):
        response = self.app.get('auth/user/f26d75e4-3bb7-41c0-8e87-87aea01b').json
        # self.assertEqual(response, [])
        self.assertEqual(response, [])


    def test_create_user(self):
        data = {
                "email": 'Jimmy@jimmy.com',
                "full_name": 'Jimmy',
                "password": 'password',
                }
        response = self.app.post('auth/register', json=data).json
        self.assertEqual(response['email'], data['email'])

    def test_delete_user_by_wrong_id(self):
        response = self.app.delete('auth/user/f26d75e4-3bb7-41c0-8e87-87aea01bd95').json
        expected_result = {"message": 'User is not found'}
        self.assertEqual(response, expected_result)

    def test_delete_user_by_id(self):
        response = self.app.delete('auth/user/f26d75e4-3bb7-41c0-8e87-87aea01bd953').json
        expected_result = {"message": "User is deleted"}
        self.assertEqual(response, expected_result)

    def test_create_user_wrong_email(self):
        data = {
            "email": 'Jimmyjimmy.com',
            "full_name": 'Jimmy',
            "password": 'password',
        }
        response = self.app.post('auth/register', json=data).json
        expected_result = {"message": 'Wrong password or email'}
        self.assertEqual(response, expected_result)

    def test_create_user_wrong_password(self):
        data = {
            "email": 'Jimmy@jimmy.com',
            "full_name": 'Jimmy',
            "password": 'pas',
        }
        response = self.app.post('auth/register', json=data).json
        expected_result = {"message": 'Wrong password or email'}
        self.assertEqual(response, expected_result)

    def test_create_user_already_exists(self):
        data = {
            "email": 'John@john.com',
            "full_name": 'John',
            "password": 'password',
        }
        response = self.app.post('auth/register', json=data).json
        expected_result = {"message": 'User already exists!'}
        self.assertEqual(response, expected_result)

    def test_create_user_wrong_data(self):
        data = {
            "em": 'John@john.com',
            "ful": 'John',
            "passw": 'password',
        }
        response = self.app.post('auth/register', json=data).json
        expected_result = {"message": 'Wrong data'}
        self.assertEqual(response, expected_result)

    def test_login_right_user(self):
        data = {
            "email": 'John@john.com',
            "password": 'password',
        }
        response = self.app.post('auth/login', json=data).json
        expected_result = 'access_token' in response.keys()
        expected_result2 = 'refresh_token' in response.keys()
        self.assertEqual(len(response.keys()), 2)
        self.assertEqual(expected_result, True)
        self.assertEqual(expected_result2, True)
        self.assertEqual(type(response['access_token']), str)
        self.assertEqual(type(response['refresh_token']), str)

    def test_login_user_not_exist(self):
        data = {
            "email": 'John@.com',
            "password": 'password',
        }
        response = self.app.post('auth/login', json=data).json
        expected_result = {"message":"Email or password is wrong"}
        self.assertEqual(response, expected_result)

    def test_login_user_wrong_password(self):
        data = {
            "email": 'John@john.com',
            "password": 'passwo',
        }
        response = self.app.post('auth/login', json=data).json
        expected_result = {"message": "Email or password is wrong"}
        self.assertEqual(response, expected_result)

    def test_login_user_wrong_data_email(self):
        data = {
            "em": 'John@.com',
            "password": 'password',
        }
        response = self.app.post('auth/login', json=data).json
        expected_result = {"message": 'Wrong data'}
        self.assertEqual(response, expected_result)

    def test_login_user_wrong_data_password(self):
        data = {
            "email": 'John@.com',
            "passw": 'password',
        }
        response = self.app.post('auth/login', json=data).json
        expected_result = {"message": 'Wrong data'}
        self.assertEqual(response, expected_result)

    def test_logout(self):
        response = self.app.post('auth/logout').json
        expected_result = {"access_token": "", 'refresh_token': ""}
        self.assertEqual(response, expected_result)

    def test_refresh_token(self):
        data = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODg3NTQ3OC"
                                 "wianRpIjoiZGQ3MzdjMjktMTMwNi00NGM1LWI5NTYtMzU1YmIzOWYzOWYwIiwidHlwZSI6InJlZnJlc2giLCJz"
                                 "dWIiOiJKZWNrQC5jb20iLCJuYmYiOjE3MDg4NzU0NzgsImNzcmYiOiI4ZGRjOTc4Mi1hOWFhLTRkN2ItYTM0MS"
                                 "1iZjdmMmFkNjJkYjMiLCJleHAiOjE3MTE0Njc0Nzh9.yJRRN20Ka98xUpOiDNSfk-N16VMKswo8hjJ8maT5IVw"}
        response = self.app.post('auth/refresh', headers=data).json
        expected_result = 'access_token' in response.keys()
        expected_result2 = 'refresh_token' in response.keys()
        self.assertEqual(len(response.keys()), 2)
        self.assertEqual(expected_result, True)
        self.assertEqual(expected_result2, True)
        self.assertEqual(type(response['access_token']), str)
        self.assertEqual(type(response['refresh_token']), str)

    def test_refresh_wrong_token(self):
        data = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODg3NTQ3OC"
                                 "wianRpIjoiZGQ3MzdjMjktMTMwNi00NGM1LWI5NTYtMzU1YmIzOWYzOWYwIiwidHlwZSI6InJlZnJlc2giLCJz"
                                 "dWIiOiJKZWNrQC5jb20iLCJuYmYiOjE3MDg4NzU0NzgsImNzcmYiOiI4ZGRjOTc4Mi1hOWFhLTRkN2ItYTM0MS"
                                 "1iZjdmMmFkNjJkYjMiLCJleHAiOjE3MTE0Njc0Nzh9.yJRRN20Ka98xUpOiDNSfk-N16VMKswo8hjJ8maT5IV"}
        response = self.app.post('auth/refresh', headers=data).json
        expected_result = {"msg": "Signature verification failed"}
        self.assertEqual(response, expected_result)

    # def test_refresh_access_token(self):
    #     data = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6MTcwODg3Nzc0OC40MDIzOTMsImlhdC"
    #                              "I6MTcwODg3NTk0OCwianRpIjoiMWNiMmRmZmUtZDFiOC00NWRlLWIwMjctMmFkYjIwZjZkNzIyIiwidHlwZSI6"
    #                              "ImFjY2VzcyIsInN1YiI6IkplY2tALmNvbSIsIm5iZiI6MTcwODg3NTk0OCwiY3NyZiI6IjYyZGQ3ODlhLWJkZD"
    #                              "AtNDc4My05ZTlkLWIwNDc1ZmNlNGQyMiIsImV4cCI6MTcwODg3OTU0OH0.eE5t2hwPTtscWcl8nOwWBcQwKKvv"
    #                              "uOE2D9Vscfgkr8Q"}
    #     response = self.app.post('/refresh', headers=data).json
    #     expected_result = {"msg": "Only refresh tokens are allowed"}
    #     self.assertEqual(response, expected_result)

    def test_refresh_without_headers(self):
        response = self.app.post('auth/refresh').json
        expected_result = {"msg": "Missing Authorization Header"}
        self.assertEqual(response, expected_result)

    def test_refresh_without_bearer(self):
        data = {"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6MTcwODg3Nzc0OC40MDIzOTMsImlhdCI6MTcwO"
                                 "Dg3NTk0OCwianRpIjoiMWNiMmRmZmUtZDFiOC00NWRlLWIwMjctMmFkYjIwZjZkNzIyIiwidHlwZSI6ImFjY2V"
                                 "zcyIsInN1YiI6IkplY2tALmNvbSIsIm5iZiI6MTcwODg3NTk0OCwiY3NyZiI6IjYyZGQ3ODlhLWJkZDAtNDc4M"
                                 "y05ZTlkLWIwNDc1ZmNlNGQyMiIsImV4cCI6MTcwODg3OTU0OH0.eE5t2hwPTtscWcl8nOwWBcQwKKvvuOE2D9V"
                                 "scfgkr8Q"}
        response = self.app.post('auth/refresh', headers=data).json
        expected_result = {"msg": "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'"}
        self.assertEqual(response, expected_result)

    # def test_login_admin(self):
    #     user_Jeck = self.db1.create_user({"id": '5606bdab-ab9d-4354-a974-fbe870a54101',
    #                                            "email": 'Jeck@jeck.com',
    #                                            "full_name": 'Jane',
    #                                            "password": 'password',
    #                                            "admin": True})
    #     data = {
    #         "email": 'Jeck@jeck.com',
    #         "password": 'password',
    #     }
    #     response = self.app.post('/login', json=data).json
    #     response['access_token']