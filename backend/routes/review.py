from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from services.pylint_service import run_pylint
from services.bandit_service import run_bandit
from services.radon_service import run_radon
from services.openai_service import ai_review

review_bp = Blueprint("review", __name__)


@review_bp.route("/review/<filename>", methods=["GET"])
@jwt_required()
def review_code(filename):

    filepath = f"uploads/{filename}"

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            code = file.read()

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 404

    pylint_report = run_pylint(filepath)
    bandit_report = run_bandit(filepath)
    radon_report = run_radon(filepath)
    ai_report = ai_review(code)

    return jsonify({

        "success": True,

        "filename": filename,

        "pylint": pylint_report,

        "bandit": bandit_report,

        "radon": radon_report,

        "ai_review": ai_report

    })