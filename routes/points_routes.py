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

@bp.route('/templates/search', methods=['GET'])
def search_points_templates(user_id):
    keyword = request.args.get('keyword', '')
    limit_param = request.args.get('limit')

    # 如果没有提供limit参数，则不限制结果数量（显示所有模板）
    limit = int(limit_param) if limit_param is not None else None

    templates = mongo_service.search_points_templates(keyword, limit)
    return jsonify(templates)
