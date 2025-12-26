from flask import Blueprint, jsonify, request
from services.mongo_service import MongoService

bp = Blueprint('stats', __name__, url_prefix='/api/stats')
mongo_service = MongoService()

@bp.route('/level-distribution', methods=['GET'])
def get_level_distribution():
    distribution = mongo_service.get_level_distribution()
    return jsonify(distribution)

@bp.route('/equipment-type-distribution', methods=['GET'])
def get_equipment_type_distribution():
    distribution = mongo_service.get_equipment_type_distribution()
    return jsonify(distribution)

@bp.route('/points-ranking', methods=['GET'])
def get_points_ranking():
    limit = request.args.get('limit', default=10, type=int)
    ranking = mongo_service.get_points_ranking(limit)
    # 转换ObjectId类型
    for user in ranking:
        user["_id"] = str(user["_id"])
    return jsonify(ranking)
