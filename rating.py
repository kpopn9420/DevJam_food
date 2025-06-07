from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime

rating_bp = Blueprint('rating', __name__)
DB_PATH = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@rating_bp.route('/rate', methods=['POST'])
def rate_user():
    try:
        data = request.get_json()
        from_user = data['from_user']
        to_user = data['to_user']
        rsv_id = data['rsv_id']
        score = data['score']
        comment = data['comment']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO ratings (from_user, to_user, rsv_id, score, comment, creat_at) VALUES (?, ?, ?, ?, ?, ?)',
            (from_user, to_user, rsv_id, score, comment, datetime.utcnow())
        )
        conn.commit()
        conn.close()

        return jsonify({'message': 'Rating submitted successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rating_bp.route('/ratings/<int:user_id>', methods=['GET'])
def get_user_ratings(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM ratings WHERE to_user = ? ORDER BY creat_at DESC',
            (user_id,)
        )
        ratings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(ratings), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
