from flask import Blueprint, request, jsonify
from ..models import LivePrediction, db

dashboard_bp = Blueprint("dashboard", __name__)

