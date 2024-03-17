from flask import Flask, request, jsonify, Blueprint

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request

from functools import wraps
from flask_jwt_extended import get_jwt
from datetime import timedelta
from business_logic import BL


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
blclass = BL()


# TODO: routs -> separated file (Flask Blueprint) +
@auth_bp.route("/login", methods=["POST"])
def login():  # TODO: return 200 tokens | 404 {"message": "user not found"}
    data = request.get_json()
    user = blclass.get_user_by_email_password(data)
    if user and len(user) > 2:
        additional_claims = {"is_admin": user['admin']}
        access_token = create_access_token(identity=data['email'], additional_claims=additional_claims,
                                           fresh=timedelta(minutes=30))
        refresh_token = create_refresh_token(identity=data['email'])
        return jsonify(access_token=access_token, refresh_token=refresh_token)
    else:
        return user


@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"access_token": "", "refresh_token": ""})
    return response


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()  # TODO: try ... except return 403 {"message": "access denied"}
    access_token = create_access_token(identity=identity, fresh=timedelta(minutes=30))
    refresh_token = create_refresh_token(identity=identity)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


# @app.route("/admin", methods=["GET"])
# @jwt_required()
# @admin_required
# def admin_hello():
#     admin = get_jwt().get('is_admin')
#     print(admin, '@@@@@@@@@@@@@@@')
#     if admin:
#         return jsonify(admin=admin)
#     else:
#         return jsonify(message='Only admin')


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403
        return decorator
    return wrapper


@auth_bp.route("/admin", methods=["GET"])
@admin_required()
def admin_hello():
    return jsonify(message="Hello admin")


@auth_bp.route('/register', methods=['POST'])
def create_user_profile():
    data = request.get_json()
    response = blclass.create_user(data)
    return response


@auth_bp.route('/user/<userid>', methods=['GET', 'DELETE'])
def get_delete_user_profile(userid):  # TODO: get_delete +
    if request.method == 'DELETE':
        response = blclass.delete_user_by_id(userid)
        return response
    user = blclass.get_user_by_id(userid)
    return user


@auth_bp.route('/user/')
def get_all_user_profiles():  # TODO: get +
    users = blclass.get_all_users()
    return users
