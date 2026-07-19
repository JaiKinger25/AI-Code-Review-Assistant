import os
from datetime import timedelta

class Config:
    SECRET_KEY = "super-secret-key"

    JWT_SECRET_KEY = "this-is-a-very-long-jwt-secret-key-123456789"

    # Token valid for 7 days
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    SQLALCHEMY_DATABASE_URI = "sqlite:///code_review.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "uploads"
    REPORT_FOLDER = "reports"