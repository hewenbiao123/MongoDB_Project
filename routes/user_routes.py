from flask import Blueprint, request, jsonify, render_template
from services.mongo_service import MongoService
from bson.objectid import ObjectId
from datetime import datetime

bp = Blueprint('user', __name__, url_prefix='/api/users')
mongo_service = MongoService()

@bp.route('/', methods=['GET'])
def get_users():
    users = mongo_service.get_all_users()
    return jsonify([{
        "id": str(user["_id"]),
        "username": user["username"],
        "nickname": user["nickname"],
        "level": user["level"],
        "experience": user.get("experience", 0),
        "registration_time": user["registration_time"].isoformat()
    } for user in users])

@bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = mongo_service.get_user_by_id(user_id)
    if user:
        user["id"] = str(user["_id"])
        user["_id"] = str(user["_id"])
        # 转换所有ObjectId和ISODate类型
        for equip in user.get("equipment", []):
            equip["_id"] = str(equip["_id"])
            equip["acquisition_time"] = equip["acquisition_time"].isoformat()
        
        for history in user.get("points", {}).get("history", []):
            history["_id"] = str(history["_id"])
            history["time"] = history["time"].isoformat()
            
        user["registration_time"] = user["registration_time"].isoformat()
        user["last_login_time"] = user["last_login_time"].isoformat()
        
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@bp.route('/', methods=['POST'])
def create_user():
    user_data = request.get_json()
    # 设置默认值
    user_data.setdefault("level", 1)
    user_data.setdefault("experience", 0)
    user_data["registration_time"] = datetime.now()
    user_data["last_login_time"] = datetime.now()
    user_data.setdefault("equipment", [])
    user_data.setdefault("points", {
        "total": 0,
        "history": []
    })
    
    user_id = mongo_service.create_user(user_data)
    return jsonify({"id": str(user_id)}), 201

@bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    update_data = request.get_json()
    # 不允许更新某些字段
    update_data.pop("registration_time", None)
    update_data.pop("equipment", None)
    update_data.pop("points", None)
    
    result = mongo_service.update_user(user_id, update_data)
    if result:
        return jsonify({"success": True})
    return jsonify({"error": "User not found or no changes made"}), 404

@bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = mongo_service.delete_user(user_id)
    if result:
        return jsonify({"success": True})
    return jsonify({"error": "User not found"}), 404
