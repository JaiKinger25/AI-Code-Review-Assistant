from datetime import timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from database import db, bcrypt
from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({
            "message": "Email already exists"
        }), 400

    hashed = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user = User(
        name=data["name"],
        email=data["email"],
        password_hash=hashed
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User Registered Successfully"
    })


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if not user:
        return jsonify({
            "message": "Invalid Email"
        }), 401

    if not bcrypt.check_password_hash(
        user.password_hash,
        data["password"]
    ):
        return jsonify({
            "message": "Wrong Password"
        }), 401

    token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=8)
    )

    return jsonify({
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    })