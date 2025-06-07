# reservation_routes.py - 修復版本

from flask import Blueprint, request, jsonify
from models import db, Food, Reservation, User
from datetime import datetime

reservation_bp = Blueprint('reservation', __name__)

# 🔥 主要修復：確保路由名稱一致，並添加錯誤處理

@reservation_bp.route('/api/reservations', methods=['POST'])
def create_reservation():
    """建立新的預約"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': '請提供 JSON 資料'}), 400
            
        # 檢查必要欄位
        required_fields = ['food_id', 'user_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'status': 'error', 
                'message': f'缺少必要欄位: {", ".join(missing_fields)}'
            }), 400

        food_id = data['food_id']
        user_id = data['user_id']
        
        # 驗證資料型別
        if not isinstance(food_id, int) or not isinstance(user_id, int):
            return jsonify({'status': 'error', 'message': 'food_id 和 user_id 必須為整數'}), 400

        # 檢查用戶是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': '用戶不存在'}), 404

        # 檢查食物是否存在且可預約
        food = Food.query.get(food_id)
        if not food:
            return jsonify({'status': 'error', 'message': '食物不存在'}), 404
            
        if food.status != 'available':
            return jsonify({'status': 'error', 'message': '食物已被預約或不可用'}), 409

        # 檢查食物是否已過期
        if food.expire_time < datetime.utcnow():
            return jsonify({'status': 'error', 'message': '食物已過期，無法預約'}), 409

        # 檢查用戶是否為食物擁有者（不能預約自己的食物）
        if food.owner_id == user_id:
            return jsonify({'status': 'error', 'message': '不能預約自己發布的食物'}), 409

        # 檢查是否已經預約過這個食物
        existing_reservation = Reservation.query.filter_by(
            food_id=food_id, 
            receiver_id=user_id,
            status='reserved'
        ).first()
        if existing_reservation:
            return jsonify({'status': 'error', 'message': '您已經預約過這個食物'}), 409

        # 建立預約
        reservation = Reservation(
            food_id=food_id,
            owner_id=food.owner_id,
            receiver_id=user_id,
            reserve_time=datetime.utcnow(),
            status='reserved'
        )
        
        # 更新食物狀態
        food.status = 'reserved'
        
        # 儲存到資料庫
        db.session.add(reservation)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': '預約成功',
            'reservation_id': reservation.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'伺服器錯誤: {str(e)}'
        }), 500

# 🔥 添加 OPTIONS 處理（解決 CORS 問題）
@reservation_bp.route('/api/reservations', methods=['OPTIONS'])
def handle_reservations_options():
    """處理 CORS preflight 請求"""
    response = jsonify()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

# GET /api/reservations
@reservation_bp.route('/api/reservations', methods=['GET'])
def list_reservations():
    """取得所有預約記錄"""
    try:
        reservations = Reservation.query.all()
        return jsonify([r.to_dict() for r in reservations])
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'無法取得預約記錄: {str(e)}'
        }), 500

# GET /api/reservations/<int:id>
@reservation_bp.route('/api/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    """取得單筆預約記錄"""
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        return jsonify(reservation.to_dict())
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'無法取得預約記錄: {str(e)}'
        }), 500

# PUT /api/reservations/<int:id>
@reservation_bp.route('/api/reservations/<int:reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    """更新預約記錄"""
    try:
        data = request.get_json() or {}
        reservation = Reservation.query.get_or_404(reservation_id)
        
        # 可更新的欄位
        if 'status' in data:
            valid_statuses = ['reserved', 'completed', 'cancelled']
            if data['status'] not in valid_statuses:
                return jsonify({
                    'status': 'error',
                    'message': f'無效的狀態值，允許的值: {", ".join(valid_statuses)}'
                }), 400
            reservation.status = data['status']
            
        if 'scheduled_pickup_time' in data:
            try:
                reservation.scheduled_pickup_time = datetime.fromisoformat(data['scheduled_pickup_time'])
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': 'scheduled_pickup_time 日期格式錯誤'
                }), 400
                
        if 'des' in data:
            reservation.des = data['des']

        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '預約更新成功',
            'reservation': reservation.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'更新失敗: {str(e)}'
        }), 500

# DELETE /api/reservations/<int:id>
@reservation_bp.route('/api/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    """刪除/取消預約"""
    try:
        reservation = Reservation.query.get_or_404(reservation_id)
        
        # 如果預約被刪除，需要把食物狀態改回 available
        food = Food.query.get(reservation.food_id)
        if food and food.status == 'reserved':
            food.status = 'available'
            
        db.session.delete(reservation)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '預約已取消'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'取消預約失敗: {str(e)}'
        }), 500

@reservation_bp.route('/api/my_reservations', methods=['GET'])
def my_reservations():
    """取得用戶的預約記錄"""
    try:
        user_id = request.args.get('user_id', type=int)
        if user_id is None:
            return jsonify({'status': 'error', 'message': '缺少 user_id 參數'}), 400
            
        # 檢查用戶是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': '用戶不存在'}), 404
            
        reservations = Reservation.query.filter_by(receiver_id=user_id).all()
        
        result = []
        for r in reservations:
            food = Food.query.get(r.food_id)
            reservation_data = {
                'id': r.id,
                'food_id': r.food_id,
                'food_name': food.name if food else '未知',
                'reserve_time': r.reserve_time.isoformat(),
                'status': r.status,
                'scheduled_pickup_time': r.scheduled_pickup_time.isoformat() if r.scheduled_pickup_time else None
            }
            result.append(reservation_data)
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'無法取得預約記錄: {str(e)}'
        }), 500

@reservation_bp.route('/api/confirm_pickup', methods=['POST'])
def confirm_pickup():
    """確認取餐完成"""
    try:
        data = request.get_json()
        if not data or 'reservation_id' not in data:
            return jsonify({'status': 'error', 'message': '缺少 reservation_id'}), 400

        reservation_id = data['reservation_id']
        if not isinstance(reservation_id, int):
            return jsonify({'status': 'error', 'message': 'reservation_id 必須為整數'}), 400

        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return jsonify({'status': 'error', 'message': '找不到預約紀錄'}), 404

        # 更新預約狀態
        reservation.status = 'completed'
        reservation.actual_pickup_time = datetime.utcnow()
        
        # 更新食物狀態
        food = Food.query.get(reservation.food_id)
        if food:
            food.status = 'done'
            
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '取餐確認完成'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'確認取餐失敗: {str(e)}'
        }), 500

# 🔥 新增：處理所有 reservation 相關路由的 OPTIONS
@reservation_bp.route('/api/reservations/<int:reservation_id>', methods=['OPTIONS'])
@reservation_bp.route('/api/my_reservations', methods=['OPTIONS'])
@reservation_bp.route('/api/confirm_pickup', methods=['OPTIONS'])
def handle_options():
    """處理 CORS preflight 請求"""
    response = jsonify()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response