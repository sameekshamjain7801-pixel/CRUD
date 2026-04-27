"""
Home/main routes.
"""
from flask import Blueprint, render_template, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Render main application page"""
    return render_template("index.html")


@main_bp.route("/health")
def health():
    """Health check endpoint for monitoring"""
    return jsonify({"status": "healthy"}), 200
