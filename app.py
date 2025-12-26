from flask import Flask, render_template, request, jsonify
from routes import user_routes, equipment_routes, points_routes, stats_routes
from services.mongo_service import MongoService
import config

app = Flask(__name__)

# 初始化MongoDB服务
mongo_service = MongoService(
    host=config.MONGO_HOST,
    port=config.MONGO_PORT,
    db_name=config.MONGO_DB_NAME
)

# 注册路由
app.register_blueprint(user_routes.bp)
app.register_blueprint(equipment_routes.bp)
app.register_blueprint(points_routes.bp)
app.register_blueprint(stats_routes.bp)

@app.route('/')
def index():
    return render_template('index.html')

# 添加统计页面路由
@app.route('/stats')
def stats():
    return render_template('stats.html')

# 添加用户详情页面路由
@app.route('/user/<user_id>')
def user_detail(user_id):
    return render_template('user_detail.html', user_id=user_id)

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
