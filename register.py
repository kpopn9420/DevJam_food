from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import bcrypt
from datetime import datetime
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
    user = verify_firebase_token(token)
    if not user:
        return jsonify({'error': 'Invalid token'}), 401

    email = user.get('email')
    name = user.get('name', '')
    uid = user['uid']
    provider = user.get('firebase', {}).get('sign_in_provider', 'firebase')

    # 嘗試將該使用者存入資料庫（若已存在就不動作）
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing = cursor.fetchone()

        if not existing:
            cursor.execute('''
                INSERT INTO users (email, passwd, name, role, addr, creat_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                email,
                'firebase',
                name,
                'user',
                '由 Firebase 建立',
                datetime.utcnow()
            ))
            conn.commit()
        conn.close()
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

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (email, passwd, name, role, addr, creat_at) VALUES (?, ?, ?, ?, ?, ?)',
            (email, hashed_pw, name, role, addr, datetime.utcnow())
        )
        conn.commit()
        conn.close()

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

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(passwd.encode('utf-8'), user['passwd']):
            return jsonify({'user_id': user['id']}), 200
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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, name, role, addr, creat_at FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify(dict(user)), 200
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
