from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from bson.objectid import ObjectId
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoService:
    def __init__(self, host='localhost', port=27017, db_name='game_db'):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None
        self.users_collection = None
        self.connected = False
        
        # 尝试连接数据库
        self.connect()
    
    def connect(self):
        try:
            self.client = MongoClient(
                self.host, 
                self.port, 
                serverSelectionTimeoutMS=5000  # 5秒超时
            )
            # 尝试获取服务器信息，验证连接
            self.client.server_info()
            self.db = self.client[self.db_name]
            self.users_collection = self.db['users']
            self.equipments_collection = self.db['equipments']
            self.points_collection = self.db['points']
            self.connected = True
            logger.info("成功连接到MongoDB数据库")
        except ServerSelectionTimeoutError:
            logger.error("无法连接到MongoDB数据库，请确保MongoDB服务正在运行")
            self.connected = False
        except Exception as e:
            logger.error(f"连接MongoDB数据库时发生错误: {str(e)}")
            self.connected = False
        
    def get_user_by_id(self, user_id):
        if not self.connected:
            return None
        return self.users_collection.find_one({"_id": ObjectId(user_id)})
        
    def get_user_by_username(self, username):
        if not self.connected:
            return None
        return self.users_collection.find_one({"username": username})
        
    def get_all_users(self):
        if not self.connected:
            return []
        return list(self.users_collection.find())
        
    def create_user(self, user_data):
        if not self.connected:
            return None
        result = self.users_collection.insert_one(user_data)
        return result.inserted_id
        
    def update_user(self, user_id, update_data):
        if not self.connected:
            return 0
        result = self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count
        
    def delete_user(self, user_id):
        if not self.connected:
            return 0
        result = self.users_collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count
        
    def add_equipment(self, user_id, equipment_data):
        if not self.connected:
            return 0
        result = self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"equipment": equipment_data}}
        )
        return result.modified_count
        
    def update_equipment(self, user_id, equipment_id, update_data):
        if not self.connected:
            return 0
        result = self.users_collection.update_one(
            {"_id": ObjectId(user_id), "equipment._id": ObjectId(equipment_id)},
            {"$set": {"equipment.$": update_data}}
        )
        return result.modified_count
        
    def delete_equipment(self, user_id, equipment_id):
        if not self.connected:
            return 0
        result = self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"equipment": {"_id": ObjectId(equipment_id)}}}
        )
        return result.modified_count
        
    def update_points(self, user_id, change, reason):
        if not self.connected:
            return 0
        # 原子操作更新积分
        result = self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            [
                {"$set": {
                    "points.total": {"$add": ["$points.total", change]},
                    "points.history": {
                        "$concatArrays": [
                            "$points.history",
                            [{"_id": ObjectId(), "change": change, "reason": reason, "time": "$$NOW"}]
                        ]
                    }
                }}
            ]
        )
        return result.modified_count
        
    def get_level_distribution(self):
        if not self.connected:
            return []
        pipeline = [
            {"$group": {"_id": "$level", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        return list(self.users_collection.aggregate(pipeline))
        
    def get_equipment_type_distribution(self):
        if not self.connected:
            return []
        pipeline = [
            {"$unwind": "$equipment"},
            {"$group": {"_id": "$equipment.type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        return list(self.users_collection.aggregate(pipeline))
        
    def get_points_ranking(self, limit=10):
        if not self.connected:
            return []
        pipeline = [
            {"$sort": {"points.total": -1}},
            {"$limit": limit},
            {"$project": {
                "_id": 1,
                "username": 1,
                "nickname": 1,
                "points.total": 1
            }}
        ]
        return list(self.users_collection.aggregate(pipeline))

    def search_equipment_templates(self, keyword, limit=None):
        """搜索装备模板"""
        if not self.connected:
            return []

        # 使用正则表达式进行模糊匹配
        query = {
            "name": {"$regex": keyword, "$options": "i"}  # 不区分大小写
        }

        # 限制返回字段
        projection = {
            "name": 1,
            "type": 1,
            "level": 1,
            "attack": 1,
            "defense": 1
        }

        # 执行查询，如果提供了limit则限制结果数量
        if limit is not None:
            results = list(self.equipments_collection.find(query, projection).limit(limit))
        else:
            results = list(self.equipments_collection.find(query, projection))

        # 将ObjectId转换为字符串
        for item in results:
            if "_id" in item:
                item["_id"] = str(item["_id"])

        return results

    def search_points_templates(self, keyword, limit=None):
        """搜索积分变动模板"""
        if not self.connected:
            return []

        # 使用正则表达式进行模糊匹配
        query = {
            "reason": {"$regex": keyword, "$options": "i"}  # 不区分大小写
        }
        logger.info(f"构建查询条件: {query}")

        # 限制返回字段
        projection = {
            "reason": 1,
            "change": 1
        }

        # 执行查询，如果提供了limit则限制结果数量
        if limit is not None:
            results = list(self.points_collection.find(query, projection).limit(limit))
        else:
            results = list(self.points_collection.find(query, projection))

        # 将ObjectId转换为字符串
        for item in results:
            if "_id" in item:
                item["_id"] = str(item["_id"])

        return results
