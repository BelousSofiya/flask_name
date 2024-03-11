import psycopg2
from uuid import uuid4
# from flask import jsonify
from validators import *
from werkzeug.security import generate_password_hash, check_password_hash

# TODO: refactor to layers
class DataBaseClass:  # TODO: "Class" is extra
    def __init__(self, **kwargs):
        with psycopg2.connect(**kwargs) as conn:
            self.conn = conn

    def initial_connect_with_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
                            id VARCHAR(100) PRIMARY KEY,
                            email VARCHAR(30),
                            full_name VARCHAR(30),
                            password VARCHAR(300),
                            admin BOOLEAN NOT NULL
                            )""")

    @staticmethod
    def zip_lists_for_user_dict(user_list):  # TODO: format_user_record(db_record) -> UserRecord:
        user_fields = ["id", "email", "full_name", "password", "admin"]
        user_dict = dict(zip(user_fields, user_list))
        user_dict.pop("password")
        return user_dict

    def get_user_by_email(self, email):
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM users WHERE email = '{email}'""")
            return cur.fetchall()

    def create_user_in_db(self, data):
        user_id = str(uuid4())
        with self.conn.cursor() as cur:
            #     return {"message": 'User already exists!'}, 403  # TODO: 400
            # TODO: !!! SQL injection https://www.psycopg.org/docs/usage.html#transactions-control
            cur.execute(f"""INSERT INTO users
                    ("id", "email", "full_name", "password", "admin")
                    VALUES('{user_id}', '{data['email']}', '{data['full_name']}', '{generate_password_hash(data['password'])}', {False})""")
            cur.execute(f"""SELECT * FROM users WHERE id = '{user_id}'""")
            self.conn.commit()
            user = cur.fetchall()[0]
            return user

    def get_user_by_id_in_db(self, user_id):  # TODO: return user | None
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM users WHERE id = '{user_id}'""")
            user = cur.fetchall()  # TODO: fetchone()
            return user

    # def get_user_by_email_password_in_db(self, data):
    #     with self.conn.cursor() as cur:
    #         email = data['email']
    #         password = data['password']
    #         # except KeyError:
    #         #     return {"message": 'Wrong data'}, 404
    #         return self.get_user_by_email(email)
    #         # cur.execute(f"""SELECT * FROM users WHERE email = '{email}'""")
    #         # user_list = cur.fetchall()
    #         # if user_list:
    #         #     user = self.zip_lists_for_user_dict(user_list[0])
    #         #     if user and check_password_hash(user_list[0][3], password):
    #         #         return user
    #         #     else:
    #         #         return {"message": "Email or password is wrong"}, 404
    #         # else:
            #     return {"message": "Email or password is wrong"}, 404

    def get_all_users_in_db(self):
        with self.conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM users""")
            users = cur.fetchall()
            return users  # TODO: map with format_user

    def delete_user_by_id_in_db(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(f"""DELETE FROM users WHERE id = '{user_id}'""")
            self.conn.commit()

    # def reset_password_in_db(self, email, password):
    #     with self.conn.cursor() as cur:
    #         cur.execute(f"""SELECT * FROM users WHERE email = '{email}'""")
    #         user = cur.fetchall()
    #         if user:
    #             cur.execute(f"""UPDATE users SET password = '{generate_password_hash(password)}' WHERE email = '{email}'""")
    #             self.conn.commit()
    #             return {"message": 'Reset password'}
    #         else:
    #             return {"message": 'User is not found '}
