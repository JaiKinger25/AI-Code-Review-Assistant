from flask import Flask
from flask_cors import CORS

from config import Config
from database import db, bcrypt, jwt, migrate

# Import Models
from models.user import User
from models.project import Project
from models.review import Review
from models.finding import Finding

# Import Blueprints
from routes.auth import auth_bp
from routes.upload import upload_bp
from routes.review import review_bp

app = Flask(__name__)

# Load Configuration
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Initialize Extensions
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

# ===========================
# JWT Error Handlers
# ===========================

@jwt.unauthorized_loader
def unauthorized_callback(reason):
    print("\n========== JWT UNAUTHORIZED ==========")
    print(reason)
    print("======================================\n")
    return {
        "success": False,
        "message": reason
    }, 401


@jwt.invalid_token_loader
def invalid_token_callback(reason):
    print("\n========== JWT INVALID TOKEN ==========")
    print(reason)
    print("=======================================\n")
    return {
        "success": False,
        "message": reason
    }, 422


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print("\n========== JWT EXPIRED ==========")
    print(jwt_payload)
    print("=================================\n")
    return {
        "success": False,
        "message": "Token expired"
    }, 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    print("\n========== JWT REVOKED ==========")
    print(jwt_payload)
    print("=================================\n")
    return {
        "success": False,
        "message": "Token has been revoked"
    }, 401


@jwt.needs_fresh_token_loader
def fresh_token_callback(jwt_header, jwt_payload):
    print("\n========== FRESH TOKEN REQUIRED ==========")
    print(jwt_payload)
    print("==========================================\n")
    return {
        "success": False,
        "message": "Fresh token required"
    }, 401

# ===========================
# Register Blueprints
# ===========================

app.register_blueprint(
    auth_bp,
    url_prefix="/api/auth"
)

app.register_blueprint(
    upload_bp,
    url_prefix="/api"
)

app.register_blueprint(
    review_bp,
    url_prefix="/api"
)

# ===========================
# Routes
# ===========================

@app.route("/")
def home():
    return {
        "status": "success",
        "message": "AI Code Review Assistant API Running 🚀"
    }


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False
    )