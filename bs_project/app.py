from flask import Flask, request, jsonify, Blueprint
from uuid import uuid4
from db_requests import *
from mail_password import *
import os

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
# from flask_jwt_extended import verify_jwt_refresh_token_in_request
from routes_authentication_users import auth_bp

from functools import wraps
# from flask_jwt_extended import set_access_cookies
# from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt
# from datetime import datetime
from datetime import timedelta
# from datetime import timezone
# from flask_mail import Mail


#config
DEBUG = True
SECRET_KEY = 'xfghtdy768oj@#$fgh%$^'  # TODO: take from env
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 465
# MAIL_USE_SSL = True
# MAIL_USERNAME = "egiksonya@gmail.com"
# MAIL_PASSWORD = "sonya1985"


# mail = Mail()
app = Flask(__name__)
# mail.init_app(app)
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = "egiksonya@gmail.com"
# app.config['MAIL_PASSWORD'] = "sonya1985"

app.config["JWT_SECRET_KEY"] = "hubahuba"  # TODO: take from env
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# mail = Mail(app)

jwt = JWTManager(app)

# def connect_db():
#     if os.getenv('TESTING').strip() == 'True':
#         return DataBaseClass(database="testing_db", host="localhost", user="postgres", password="postgres", port="5432")
#     else:
#         return DataBaseClass(database="flask_bs_db", host="localhost", user="postgres", password="postgres", port="5432")
#
#
# db = connect_db()
# db.initial_connect_with_db()

app.register_blueprint(auth_bp)
# @app.route("/reset_password", methods=["GET"])
# def reset_password():
#     data = request.get_json()
#     email = data['email']
#     password = password_generator(12)
#     msg = f"Your new password: {password}"
#     db.reset_password_in_db(email, password)
#     with app.app_context():
#         mail.send(msg)

# # TODO: routs -> separated file (Flask Blueprint)
# @app.route("/login", methods=["POST"])
# def login():  # TODO: return 200 tokens | 404 {"message": "user not found"}
#     data = request.get_json()
#     user = db.get_user_by_email_password(data)
#     if user and len(user) > 2:
#         additional_claims = {"is_admin": user['admin']}
#         access_token = create_access_token(identity=data['email'], additional_claims=additional_claims,
#                                            fresh=timedelta(minutes=30))
#         refresh_token = create_refresh_token(identity=data['email'])
#         return jsonify(access_token=access_token, refresh_token=refresh_token)
#     else:
#         return user
#
#
# @app.route("/logout", methods=["POST"])
# def logout():
#     response = jsonify({"access_token": "", "refresh_token": ""})
#     return response
#
#
# @app.route("/refresh", methods=["POST"])
# @jwt_required(refresh=True)
# def refresh():
#     identity = get_jwt_identity()  # TODO: try ... except return 403 {"message": "access denied"}
#     access_token = create_access_token(identity=identity, fresh=timedelta(minutes=30))
#     refresh_token = create_refresh_token(identity=identity)
#     return jsonify(access_token=access_token, refresh_token=refresh_token)
#
#
# # @app.route("/admin", methods=["GET"])
# # @jwt_required()
# # @admin_required
# # def admin_hello():
# #     admin = get_jwt().get('is_admin')
# #     print(admin, '@@@@@@@@@@@@@@@')
# #     if admin:
# #         return jsonify(admin=admin)
# #     else:
# #         return jsonify(message='Only admin')
#
#
# def admin_required():
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             verify_jwt_in_request()
#             claims = get_jwt()
#             if claims["is_admin"]:
#                 return fn(*args, **kwargs)
#             else:
#                 return jsonify(msg="Admins only!"), 403
#         return decorator
#     return wrapper
#
#
# @app.route("/admin", methods=["GET"])
# @admin_required()
# def admin_hello():
#     return jsonify(message="Hello admin")
#
#
# @app.route('/register', methods=['POST'])
# def create_user_profile():
#     data = request.get_json()
#     response = db.create_user(data)
#     return response
#
#
# @app.route('/user/<userid>', methods=['GET', 'DELETE'])
# def show_delete_user_profile(userid):  # TODO: get_delete
#     if request.method == 'DELETE':
#         response = db.delete_user_by_id(userid)
#         return response
#     user = db.get_user_by_id(userid)
#     return user
#
#
# @app.route('/user/')
# def show_all_user_profiles():  # TODO: get
#     users = db.get_all_users()
#     return users


if __name__ == "__main__":
    app.run()
