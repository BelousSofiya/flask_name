from db_requests import DataBaseClass# as dbclass
from uuid import uuid4
# from flask import jsonify
from validators import *
from werkzeug.security import generate_password_hash, check_password_hash
import os

# dbclass = DataBaseClass()
def connect_db():
    if os.getenv('TESTING').strip() == 'True':
        return DataBaseClass(database="testing_db", host="localhost", user="postgres", password="postgres", port="5432")
    else:
        return DataBaseClass(database="flask_bs_db", host="localhost", user="postgres", password="postgres", port="5432")


db = connect_db()
db.initial_connect_with_db()


class BL:

    def format_user_record(self, user_list):  # TODO: format_user_record(db_record) -> UserRecord: +
        user_fields = ["id", "email", "full_name", "password", "admin"]
        user_dict = dict(zip(user_fields, user_list))
        user_dict.pop("password")
        return user_dict

    def create_user(self, data):
        if not validate_data_includes_email_password(data):
            return {"message": 'Wrong data'}, 404
        else:
            if not validate_email(data['email']) or not validate_password(data['password']):
                return {"message": 'Wrong password or email'}, 400  # TODO: 400 +
        user_in_db = db.get_user_by_email(data['email'])
        if user_in_db:
            return {"message": 'User already exists!'}, 403
        user_data = db.create_user_in_db(data)
        user = self.format_user_record(user_data)
        return user


    def get_user_by_id(self, user_id):  # TODO: return user | None
        #     user = cur.fetchall()  # TODO: fetchone()
        user = db.get_user_by_id_in_db(user_id)
        return self.format_user_record(user[0]) if user else user
        # return self.format_user_record(user[0]) if user else None =>  The function either returned None or ended without a return statement.



    def get_user_by_email_password(self, data):
        if not validate_data_includes_email_password(data):
            return {"message": 'Wrong data'}, 404
        email = data['email']
        password = data['password']
        user = db.get_user_by_email(email)
        if user and check_password_hash(user[0][3], password):
            return self.format_user_record(user[0])
        else:
            return {"message": "Email or password is wrong"}, 404

    def get_all_users(self):
        raw_users = db.get_all_users_in_db()
        users = [self.format_user_record(user) for user in raw_users]
        return users
        # with self.conn.cursor() as cur:
        #     cur.execute(f"""SELECT * FROM users""")
        #     users = cur.fetchall()
        #     return users  # TODO: map with format_user +


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

    def delete_user_by_id(self, user_id):
        user = db.get_user_by_id_in_db(user_id)
        if user:
            db.delete_user_by_id_in_db(user_id)
            return {"message": 'User is deleted'}
        else:
            return {"message": 'User is not found'}