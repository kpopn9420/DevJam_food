from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import bcrypt
from datetime import datetime
from models import db, Food, Reservation, User
from firebase_auth import verify_firebase_token

app = Flask(__name__)
CORS(app)

DB_PATH = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# =============================
# Firebase Token 驗證 + 自動補上資料庫帳號
# =============================
@app.route('/secure', methods=['GET'])
def secure_area():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Missing Authorization header'}), 401

    token = token.replace('Bearer ', '')
    user_data = verify_firebase_token(token)
    if not user_data:
        return jsonify({'error': 'Invalid token'}), 401

    email = user_data.get('email')
    name = user_data.get('name', '')
    uid = user_data['uid']
    provider = user_data.get('firebase', {}).get('sign_in_provider', 'firebase')

    try:
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(
                email=email,
                passwd=b'firebase',  # 當作固定值，避免 NULL 問題
                name=name,
                role='user',
                addr='由 Firebase 建立'
            )
            db.session.add(new_user)
            db.session.commit()

    except Exception as e:
        return jsonify({'error': f'Login OK, but failed to sync to DB: {str(e)}'}), 500

    return jsonify({
        'message': f'Welcome, {email}!',
        'uid': uid,
        'provider': provider
    }), 200

# =============================
# 註冊 API（本地帳號）
# =============================
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data['email']
        passwd = data['passwd']
        name = data['name']
        role = data['role']
        addr = data['addr']

        hashed_pw = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

        user = User(
            email=email,
            passwd=hashed_pw,
            name=name,
            role=role,
            addr=addr
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Registration successful'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================
# 登入 API（本地帳號）
# =============================
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        passwd = data['passwd']

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(passwd.encode('utf-8'), user.passwd):
            return jsonify({'user_id': user.id}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================
# 查詢使用者資料
# =============================
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role,
                'addr': user.addr,
                'creat_at': user.creat_at.isoformat()
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# =============================
# 匯入評價系統
# =============================
from rating import rating_bp
app.register_blueprint(rating_bp)

# =============================
# 主程式進入點
# =============================
if __name__ == '__main__':
    app.run(port=5001, debug=True)
