from flask import Blueprint, request, jsonify
from models import db, Food, Reservation
from datetime import datetime

reservation_bp = Blueprint('reservation', __name__)

@reservation_bp.route('/api/reserve_food', methods=['POST'])
def reserve_food():
    data = request.get_json() or {}
    if 'food_id' not in data or 'user_id' not in data:
        return jsonify({'status': 'error', 'message': 'food_id 和 user_id 為必填'}), 400

    food_id = data['food_id']
    user_id = data['user_id']
    if not isinstance(food_id, int) or not isinstance(user_id, int):
        return jsonify({'status': 'error', 'message': 'food_id 和 user_id 必須為整數'}), 400

    food = Food.query.get(food_id)
    if not food or food.status != 'available':
        return jsonify({'status': 'error', 'message': '該食物不可預約'}), 400

    reservation = Reservation(
        food_id=food_id,
        owner_id=food.owner_id,
        receiver_id=user_id,
        reserve_time=datetime.utcnow(),
        status='reserved'
    )
    food.status = 'reserved'
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'status': 'success', 'message': '預約成功', 'reservation_id': reservation.id})

@reservation_bp.route('/api/my_reservations', methods=['GET'])
def my_reservations():
    user_id = request.args.get('user_id', type=int)
    
    if user_id is None:
        return jsonify({'status': 'error', 'message': '缺少 user_id'}), 400
    res_list = Reservation.query.filter_by(receiver_id=user_id).all()
    data = []
    for r in res_list:
        data.append({
            'id': r.id,
            'food_id': r.food_id,
            'reserve_time': r.reserve_time.isoformat(),
            'status': r.status
        })
    return jsonify(data)

@reservation_bp.route('/api/confirm_pickup', methods=['POST'])
def confirm_pickup():
    data = request.get_json() or {}
    if 'reservation_id' not in data:
        return jsonify({'status': 'error', 'message': '缺少 reservation_id'}), 400

    reservation_id = data['reservation_id']
    if not isinstance(reservation_id, int):
        return jsonify({'status': 'error', 'message': 'reservation_id 必須為整數'}), 400

    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'status': 'error', 'message': '找不到預約紀錄'}), 404

    reservation.status = 'completed'
    food = Food.query.get(reservation.food_id)
    if food:
        food.status = 'done'
    db.session.commit()
    return jsonify({'status': 'success', 'message': '取餐確認完成'})