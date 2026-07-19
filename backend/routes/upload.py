from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models.project import Project
from database import db
import os

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@upload_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():

    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    project = Project(
        user_id=int(get_jwt_identity()),
        project_name=filename,
        upload_type="file"
    )

    db.session.add(project)
    db.session.commit()

    return jsonify({
        "message": "File uploaded successfully",
        "project_id": project.id,
        "filename": filename
    })