from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager

from routes_authentication_users import auth_bp
from config import Config


# TODO: take from env +

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run()
