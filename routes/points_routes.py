from flask import Blueprint, request, jsonify
from services.mongo_service import MongoService

bp = Blueprint('points', __name__, url_prefix='/api/users/<user_id>/points')
mongo_service = MongoService()

@bp.route('/', methods=['POST'])
def update_points(user_id):
    data = request.get_json()
    change = data.get("change")
    reason = data.get("reason", "")
    
    if change is None:
        return jsonify({"error": "Change parameter is required"}), 400
    
    result = mongo_service.update_points(user_id, change, reason)
    if result:
        return jsonify({"success": True})
    return jsonify({"error": "Failed to update points"}), 400
