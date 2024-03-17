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
from config import Config

from functools import wraps
# from flask_jwt_extended import set_access_cookies
# from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt
# from datetime import datetime
from datetime import timedelta
# from datetime import timezone
# from flask_mail import Mail


#config
# DEBUG = True
# SECRET_KEY = 'xfghtdy768oj@#$fgh%$^'  # TODO: take from env
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 465
# MAIL_USE_SSL = True
# MAIL_USERNAME = ""
# MAIL_PASSWORD = ""


# mail = Mail()
app = Flask(__name__)
# mail.init_app(app)
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = ""
# app.config['MAIL_PASSWORD'] = ""

# app.config["JWT_SECRET_KEY"] = "hubahuba"  # TODO: take from env +
# app.config["JWT_COOKIE_SECURE"] = False
# app.config["JWT_TOKEN_LOCATION"] = ["headers"]
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# mail = Mail(app)
app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run()
