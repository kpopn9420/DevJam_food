# app.py - 修復 CORS 問題

from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from models import db
from routes.food_routes import food_bp
from routes.reservation_routes import reservation_bp
from rating import rating_bp


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
db.init_app(app)

# 註冊藍圖
app.register_blueprint(food_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(rating_bp)


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
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'foods': '/api/foods',
            'reservations': '/api/reservations',
            'nearby_foods': '/api/nearby_foods',
            'available_foods': '/api/available_foods',
            'my_posted_foods': '/api/my_posted_foods',
            'my_reservations': '/api/my_reservations',
            'confirm_pickup': '/api/confirm_pickup'
        },
        'documentation': '/docs'
    })

# 建立資料表
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return jsonify({
        'message': '🍽️ FoodShare 後端服務啟動成功！',
        'api_docs': 'http://localhost:5000/docs',
        'api_root': 'http://localhost:5000/api'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)