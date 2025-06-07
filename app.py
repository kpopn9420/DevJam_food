# app.py - 修復 CORS 問題並加入地圖功能

from flask import Flask, jsonify
# app.py - 修復 CORS 問題
import bcrypt
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from models import db, init_db
from routes.food_routes import food_bp
from models import db, Food, Reservation, User
from routes.reservation_routes import reservation_bp
from rating import rating_bp
from routes.map_routes import map_bp
from flask import Flask, request, jsonify
# from firebase_auth import verify_firebase_token


app = Flask(__name__)

# # 🔥 修復 CORS 設定
# CORS(app, resources={
#     r"/api/*": {
#         "origins": "*",
#         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#         "allow_headers": ["Content-Type", "Authorization"]
#     }
# })
# CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
CORS(app) 



# Swagger UI 設定
SWAGGER_URL = "/docs"
API_URL = "/static/openapi.yaml"

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "FoodShare API"}
)
app.register_blueprint(swagger_bp, url_prefix="/docs")
# 本機 MySQL 設定（依照你自己的設定修改）
# app.py
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/foodsystem"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
    return (
        jsonify({"status": "error", "message": "找不到請求的資源", "error_code": 404}),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    return (
        jsonify({"status": "error", "message": "伺服器內部錯誤", "error_code": 500}),
        500,
    )


@app.errorhandler(400)
def bad_request(error):
    return (
        jsonify({"status": "error", "message": "請求格式錯誤", "error_code": 400}),
        400,
    )


# 🔥 添加全域 OPTIONS 處理器（作為後備）
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        return response


# 🔥 添加 API 根路徑
@app.route("/api")
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
    return jsonify(
        {
            "message": "FoodShare API",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "foods": "/api/foods",
                "reservations": "/api/reservations",
                "nearby_foods": "/api/nearby_foods",
                "available_foods": "/api/available_foods",
                "my_posted_foods": "/api/my_posted_foods",
                "my_reservations": "/api/my_reservations",
                "confirm_pickup": "/api/confirm_pickup",
            },
            "documentation": "/docs",
        }
    )


# =============================
# Firebase Token 驗證 + 自動補上資料庫帳號
# =============================
@app.route("/secure", methods=["GET"])
def secure_area():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing Authorization header"}), 401

    token = token.replace("Bearer ", "")
    user_data = verify_firebase_token(token)
    if not user_data:
        return jsonify({"error": "Invalid token"}), 401

    email = user_data.get("email")
    name = user_data.get("name", "")
    uid = user_data["uid"]
    provider = user_data.get("firebase", {}).get("sign_in_provider", "firebase")

    try:
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(
                email=email,
                passwd=b"firebase",  # 當作固定值，避免 NULL 問題
                name=name,
                role="user",
                addr="由 Firebase 建立",
            )
            db.session.add(new_user)
            db.session.commit()

    except Exception as e:
        return jsonify({"error": f"Login OK, but failed to sync to DB: {str(e)}"}), 500

    return (
        jsonify({"message": f"Welcome, {email}!", "uid": uid, "provider": provider}),
        200,
    )


# =============================
# 註冊 API（本地帳號）
# =============================
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        email = data["email"]
        passwd = data["passwd"]
        name = data["name"]
        role = data["role"]
        addr = data["addr"]

        hashed_pw = bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt())

        user = User(email=email, passwd=hashed_pw, name=name, role=role, addr=addr)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Registration successful"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================
# 登入 API（本地帳號）
# =============================
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        print("Received data:", data)

        email = data["email"]
        passwd = data["passwd"]
        print("Parsed email and password")

        user = User.query.filter_by(email=email).first()
        print("User query result:", user)

        if user and passwd == user.password_hash:
            print("Login successful")
            return jsonify({"user_id": user.id}), 200
        else:
            print("Invalid credentials")
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"error": str(e)}), 500



# =============================
# 查詢使用者資料
# =============================
@app.route("/user/<int:user_id>", methods=["GET"])
def get_user_info(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return (
                jsonify(
                    {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "role": user.role,
                        "addr": user.addr,
                        "creat_at": user.creat_at.isoformat(),
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 建立資料表
with app.app_context():
    db.create_all()


@app.route("/")
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
        


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
        # return jsonify(
        #     {
        #         "message": "🍽️ FoodShare 後端服務啟動成功！",
        #         "api_docs": "http://localhost:5000/docs",
        #         "api_root": "http://localhost:5000/api",
        #     }
        # )