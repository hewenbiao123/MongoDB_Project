from flask import Blueprint, request, jsonify
from services.mongo_service import MongoService
from bson.objectid import ObjectId
from datetime import datetime

bp = Blueprint('equipment', __name__, url_prefix='/api/users/<user_id>/equipment')
mongo_service = MongoService()

@bp.route('/', methods=['POST'])
def add_equipment(user_id):
    equipment_data = request.get_json()
    # 设置默认值
    equipment_data["_id"] = ObjectId()
    equipment_data["acquisition_time"] = datetime.now()
    
    result = mongo_service.add_equipment(user_id, equipment_data)
    if result:
        return jsonify({"success": True})
    return jsonify({"error": "Failed to add equipment"}), 400

@bp.route('/<equipment_id>', methods=['PUT'])
def update_equipment(user_id, equipment_id):
    update_data = request.get_json()
    # 不允许更新某些字段
    update_data.pop("_id", None)
    update_data.pop("acquisition_time", None)
    
    result = mongo_service.update_equipment(user_id, equipment_id, update_data)
    if result:
        return jsonify({"success": True})
    return jsonify({"error": "Failed to update equipment"}), 400

@bp.route('/<equipment_id>', methods=['DELETE'])
def delete_equipment(user_id, equipment_id):
    result = mongo_service.delete_equipment(user_id, equipment_id)
    if result:
        return jsonify({"success": True})
    return jsonify({"error": "Failed to delete equipment"}), 400
