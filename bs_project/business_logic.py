from db_requests import DataBase# as dbclass
from validators import *
from werkzeug.security import generate_password_hash, check_password_hash
import os

def connect_db():
    if os.getenv('TESTING').strip() == 'True':
        return DataBase(database="testing_db", host="localhost", user="postgres", password="postgres", port="5432")
    else:
        return DataBase(database="flask_bs_db", host="localhost", user="postgres", password="postgres", port="5432")


db = connect_db()
db.initial_connect_with_db()


class BL:

    @staticmethod
    def format_user_record(user_record):  # TODO: format_user_record(db_record) -> UserRecord: +
        user_fields = ["id", "email", "full_name", "password", "admin"]
        user = dict(zip(user_fields, user_record))
        user.pop("password")
        return user

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

    def get_user_by_id(self, user_id):
        user = db.get_user_by_id_in_db(user_id)
        return self.format_user_record(user) if user else {"message": 'User is not found'}, 400


    def get_user_by_email_password(self, data):
        if not validate_data_includes_email_password(data):
            return {"message": 'Wrong data'}, 404
        email = data['email']
        password = data['password']
        user = db.get_user_by_email(email)
        if user and check_password_hash(user[3], password):
            return self.format_user_record(user)
        else:
            return {"message": "Email or password is wrong"}, 404

    def get_all_users(self):
        raw_users = db.get_all_users_in_db()
        users = [self.format_user_record(user) for user in raw_users]
        return users # TODO: map with format_user +


    def delete_user_by_id(self, user_id):
        user = db.get_user_by_id_in_db(user_id)
        if user:
            db.delete_user_by_id_in_db(user_id)
            return {"message": 'User is deleted'}
        else:
            return {"message": 'User is not found'}