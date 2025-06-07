from flask import Blueprint, request, jsonify
from models import db, Food
import math
from datetime import datetime

food_bp = Blueprint('food', __name__)

# 工具函式：計算兩點間距離（公里）
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # 地球半徑 (公里)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@food_bp.route('/api/post_food', methods=['POST'])
def post_food():
    data = request.get_json() or {}
    required = ['owner_id', 'title', 'quantity', 'expire_time', 'lat', 'lng']
    if not all(k in data for k in required):
        return jsonify({'status': 'error', 'message': '缺少必要欄位'}), 400

    # 解析 expire_time 字串為 datetime
    try:
        expire_time = datetime.fromisoformat(data['expire_time'])
    except Exception:
        return jsonify({'status': 'error', 'message': 'expire_time 格式錯誤'}), 400

    # 建立 Food
    food = Food(
        owner_id=data['owner_id'],
        name=data['title'],
        description=data.get('description', ''),
        quantity=data['quantity'],
        expire_time=expire_time,
        lat=data['lat'],
        lng=data['lng'],
        status='available',
        category=data.get('category'),
        image_url=data.get('image_url')
    )
    db.session.add(food)
    db.session.commit()
    return jsonify({'status': 'success', 'message': '上架成功', 'food_id': food.id})

@food_bp.route('/api/nearby_foods', methods=['GET'])
def nearby_foods():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
    except (TypeError, ValueError):
        return jsonify({'status': 'error', 'message': '座標格式不正確'}), 400

    foods = Food.query.filter_by(status='available').all()
    results = []
    for f in foods:
        dist = haversine(lat, lng, f.lat, f.lng)
        results.append({
            'id': f.id,
            'title': f.name,
            'description': f.description,
            'quantity': f.quantity,
            'expire_time': f.expire_time.isoformat(),
            'owner_id': f.owner_id,
            'status': f.status,
            'category': f.category,
            'image_url': f.image_url,
            'distance': round(dist, 2)
        })
    results = sorted(results, key=lambda x: x['distance'])[:5]
    return jsonify(results)

@food_bp.route('/api/my_posted_foods', methods=['GET'])
def my_posted_foods():
    user_id = request.args.get('user_id', type=int)
    if user_id is None:
        return jsonify({'status': 'error', 'message': '缺少 user_id'}), 400
    foods = Food.query.filter_by(owner_id=user_id).all()
    data = []
    for f in foods:
        data.append({
            'id': f.id,
            'title': f.name,
            'description': f.description,
            'quantity': f.quantity,
            'expire_time': f.expire_time.isoformat(),
            'status': f.status,
            'category': f.category,
            'image_url': f.image_url
        })
    return jsonify(data)