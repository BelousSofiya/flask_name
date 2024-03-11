# from db_requests import DataBaseClass
# from uuid import uuid4
# # from flask import jsonify
# from validators import *
# from werkzeug.security import generate_password_hash, check_password_hash
#
# dbclass = DataBaseClass()
#
#
# def zip_lists_for_user_dict(user_list):  # TODO: format_user_record(db_record) -> UserRecord:
#     user_fields = ["id", "email", "full_name", "password", "admin"]
#     user_dict = dict(zip(user_fields, user_list))
#     user_dict.pop("password")
#     return user_dict
#
#
# def create_user(self, data):
#     try:
#         if not validate_email(data['email']) or not validate_password(data['password']):
#             return {"message": 'Wrong password or email'}, 404  # TODO: 400
#     except KeyError:  # validate_data_includes_email_password
#         return {"message": 'Wrong data'}, 404  # TODO: 400
#     user_data = dbclass.create_user_in_db(data)
#     user = self.zip_lists_for_user_dict(user_data)
#     return user
#
#
# def get_user_by_id(self, user_id):  # TODO: return user | None
#     with self.conn.cursor() as cur:
#         cur.execute(f"""SELECT * FROM users WHERE id = '{user_id}'""")
#         user = cur.fetchall()  # TODO: fetchone()
#         return self.zip_lists_for_user_dict(user[0]) if user else user
#
#
# def get_user_by_email_password(self, data):
#     with self.conn.cursor() as cur:
#         try:  # TODO: -> validator
#             email = data['email']
#             password = data['password']
#         except KeyError:
#             return {"message": 'Wrong data'}, 404
#         cur.execute(f"""SELECT * FROM users WHERE email = '{email}'""")
#         user_list = cur.fetchall()
#         if user_list:
#             user = self.zip_lists_for_user_dict(user_list[0])
#             if user and check_password_hash(user_list[0][3], password):
#                 return user
#             else:
#                 return {"message": "Email or password is wrong"}, 404
#         else:
#             return {"message": "Email or password is wrong"}, 404
#
#
# def get_all_users(self):
#     with self.conn.cursor() as cur:
#         cur.execute(f"""SELECT * FROM users""")
#         users = cur.fetchall()
#         return users  # TODO: map with format_user
#
#
# # def reset_password_in_db(self, email, password):
# #     with self.conn.cursor() as cur:
# #         cur.execute(f"""SELECT * FROM users WHERE email = '{email}'""")
# #         user = cur.fetchall()
# #         if user:
# #             cur.execute(f"""UPDATE users SET password = '{generate_password_hash(password)}' WHERE email = '{email}'""")
# #             self.conn.commit()
# #             return {"message": 'Reset password'}
# #         else:
# #             return {"message": 'User is not found '}
#
# def delete_user_by_id(user_id):
#     user = dbclass.get_user_by_id(user_id)
#     if user:
#         dbclass.request_delete_user_by_id(user_id)
#         # if response.status_code == 204:
#         return {"message": 'User is deleted'}
#     else:
#         return {"message": 'User is not found'}