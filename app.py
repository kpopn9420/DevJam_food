# app.py - 修復 CORS 問題並加入地圖功能

from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from models import db, init_db
from routes.food_routes import food_bp
from routes.reservation_routes import reservation_bp
from rating import rating_bp
from routes.map_routes import map_bp

app = Flask(__name__)

# 🔥 修復 CORS 設定
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Swagger UI 設定
SWAGGER_URL = '/docs'
API_URL = '/static/openapi.yaml'

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "FoodShare API"}
)
app.register_blueprint(swagger_bp, url_prefix='/docs')
# 本機 MySQL 設定（依照你自己的設定修改）
# app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/foodsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化資料庫
init_db(app)

# 註冊藍圖
app.register_blueprint(food_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(rating_bp)
app.register_blueprint(map_bp)  # 🗺️ 新增地圖功能

# 🔥 添加全域錯誤處理器
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': '找不到請求的資源',
        'error_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': '伺服器內部錯誤',
        'error_code': 500
    }), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'status': 'error',
        'message': '請求格式錯誤',
        'error_code': 400
    }), 400

# 🔥 添加全域 OPTIONS 處理器（作為後備）
@app.before_request
def handle_preflight():
    from flask import request
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

# 🔥 添加 API 根路徑
@app.route('/api')
def api_info():
    return jsonify({
        'message': 'FoodShare API',
        'version': '1.1.0',
        'status': 'running',
        'endpoints': {
            'foods': '/api/foods',
            'reservations': '/api/reservations',
            'nearby_foods': '/api/nearby_foods',
            'available_foods': '/api/available_foods',
            'my_posted_foods': '/api/my_posted_foods',
            'my_reservations': '/api/my_reservations',
            'confirm_pickup': '/api/confirm_pickup',
            # 🗺️ 地圖功能端點
            'map_nearby_foods': '/api/map/nearby_foods',
            'map_food_clusters': '/api/map/food_clusters',
            'map_area_stats': '/api/map/area_stats',
            'map_heatmap_data': '/api/map/heatmap_data',
            'map_sync_firebase': '/api/map/sync_to_firebase'
        },
        'documentation': '/docs',
        'map_test_tool': '/static/map_test.html'
    })

@app.route('/')
def index():
    return jsonify({
        'message': '🍽️ FoodShare 後端服務啟動成功！',
        'api_docs': 'http://localhost:5000/docs',
        'api_root': 'http://localhost:5000/api',
        'map_test_tool': 'http://localhost:5000/static/map_test.html'
    })

# 🗺️ 提供地圖測試工具
@app.route('/static/map_test.html')
def map_test_tool():
    """提供地圖測試工具頁面"""
    return app.send_static_file('map_test.html') if app.static_folder else jsonify({
        'error': '請將測試工具 HTML 放在 static 資料夾中'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)