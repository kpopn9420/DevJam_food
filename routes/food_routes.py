from flask import Blueprint, request, jsonify
from models import db, Food
from geo_service import GeoService
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

@food_bp.route('/api/foods', methods=['POST'])
def create_food():
    """新增食物 - 支援地址自動轉換"""
    data = request.get_json() or {}
    
    # 檢查必要欄位
    required = ['owner_id', 'title', 'quantity', 'expire_time']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({
            'status': 'error', 
            'message': f'缺少必要欄位: {", ".join(missing)}'
        }), 400

    # 處理位置資訊
    lat, lng = None, None
    location_source = None
    
    # 優先使用經緯度
    if 'lat' in data and 'lng' in data:
        try:
            lat = float(data['lat'])
            lng = float(data['lng'])
            location_source = 'coordinates'
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': '經緯度格式錯誤'
            }), 400
    
    # 如果沒有經緯度，嘗試地址轉換
    elif 'address' in data and data['address'].strip():
        address = data['address'].strip()
        # 直接使用 address，因為 GeoService 內部已處理地址清理
        geocode_result = GeoService.address_to_coordinates(address)
        if geocode_result:
            lat = geocode_result['lat']
            lng = geocode_result['lng']
            location_source = 'address'
            # 儲存格式化後的地址
            data['formatted_address'] = geocode_result['formatted_address']
        else:
            return jsonify({
                'status': 'error',
                'message': '無法找到該地址的座標',
                'address': address,
                'suggestions': [
                    '請確認地址是否正確',
                    '嘗試使用更完整的地址',
                    '或直接提供經緯度座標'
                ]
            }), 400
    else:
        return jsonify({
            'status': 'error',
            'message': '請提供地址或經緯度座標'
        }), 400

    # 驗證座標範圍
    if not (21.5 <= lat <= 25.5 and 119.5 <= lng <= 122.5):
        return jsonify({
            'status': 'error',
            'message': '座標超出台灣範圍'
        }), 400

    # 解析過期時間
    try:
        expire_time = datetime.fromisoformat(data['expire_time'])
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'expire_time 格式錯誤，請使用 ISO 格式'
        }), 400

    # 建立 Food 記錄
    food = Food(
        owner_id=data['owner_id'],
        name=data['title'],
        description=data.get('description', ''),
        quantity=data['quantity'],
        expire_time=expire_time,
        lat=lat,
        lng=lng,
        status='available',
        category=data.get('category'),
        image_url=data.get('image_url')
    )
    
    try:
        db.session.add(food)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '食物上架成功',
            'data': {
                'food_id': food.id,
                'location_source': location_source,
                'coordinates': {'lat': lat, 'lng': lng},
                'formatted_address': data.get('formatted_address')
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'資料庫錯誤: {str(e)}'
        }), 500

@food_bp.route('/api/foods', methods=['GET'])
def list_foods():
    foods = Food.query.all()
    return jsonify([f.to_dict() for f in foods])

@food_bp.route('/api/foods/<int:food_id>', methods=['GET'])
def get_food(food_id):
    food = Food.query.get_or_404(food_id)
    food_data = food.to_dict()
    
    # 如果需要，添加地址資訊
    if request.args.get('include_address') == 'true':
        address_result = GeoService.coordinates_to_address(food.lat, food.lng)
        if address_result:
            food_data['address'] = address_result['address']
    
    return jsonify(food_data)

@food_bp.route('/api/foods/<int:food_id>', methods=['PUT'])
def update_food(food_id):
    data = request.get_json() or {}
    food = Food.query.get_or_404(food_id)

    # 更新基本欄位
    if 'name' in data:
        food.name = data['name']
    if 'category' in data:
        food.category = data['category']
    if 'description' in data:
        food.description = data['description']
    if 'quantity' in data:
        food.quantity = data['quantity']
    if 'image_url' in data:
        food.image_url = data['image_url']
    
    # 更新位置
    location_updated = False
    if 'lat' in data and 'lng' in data:
        try:
            food.lat = float(data['lat'])
            food.lng = float(data['lng'])
            location_updated = True
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': '經緯度格式錯誤'
            }), 400
    elif 'address' in data and data['address'].strip():
        address = data['address'].strip()
        geocode_result = GeoService.address_to_coordinates(address)
        if geocode_result:
            food.lat = geocode_result['lat']
            food.lng = geocode_result['lng']
            location_updated = True
        else:
            return jsonify({
                'status': 'error',
                'message': '無法找到該地址的座標'
            }), 400
    
    # 更新過期時間
    if 'expire_time' in data:
        try:
            raw = data['expire_time']
            if raw.endswith('Z'):
                raw = raw[:-1] + '+00:00'
            food.expire_time = datetime.fromisoformat(raw)
        except Exception:
            return jsonify({
                'status': 'error',
                'message': '過期時間格式錯誤'
            }), 400

    try:
        db.session.commit()
        response_data = {
            'status': 'success',
            'food': food.to_dict()
        }
        if location_updated:
            response_data['location_updated'] = True
        return jsonify(response_data)
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'更新失敗: {str(e)}'
        }), 500

@food_bp.route('/api/foods/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    food = Food.query.get_or_404(food_id)
    try:
        db.session.delete(food)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'刪除失敗: {str(e)}'
        }), 500

@food_bp.route('/api/nearby_foods', methods=['GET'])
def nearby_foods():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
    except (TypeError, ValueError):
        return jsonify({
            'status': 'error',
            'message': '座標格式不正確'
        }), 400

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

@food_bp.route('/api/available_foods', methods=['GET'])
def available_foods():
    foods = Food.query.filter_by(status='available').all()
    return jsonify([
        {
            'id': f.id,
            'title': f.name,
            'category': f.category,
            'lat': f.lat,
            'lng': f.lng,
            'image_url': f.image_url,
            'expire_time': f.expire_time.isoformat()
        }
        for f in foods
    ])

@food_bp.route('/api/my_posted_foods', methods=['GET'])
def my_posted_foods():
    user_id = request.args.get('user_id', type=int)
    if user_id is None:
        return jsonify({
            'status': 'error',
            'message': '缺少 user_id'
        }), 400
    
    foods = Food.query.filter_by(owner_id=user_id).all()
    include_address = request.args.get('include_address') == 'true'
    
    data = []
    for f in foods:
        food_dict = {
            'id': f.id,
            'title': f.name,
            'description': f.description,
            'quantity': f.quantity,
            'expire_time': f.expire_time.isoformat(),
            'status': f.status,
            'category': f.category,
            'image_url': f.image_url,
            'coordinates': {'lat': f.lat, 'lng': f.lng}
        }
        
        if include_address:
            address_result = GeoService.coordinates_to_address(f.lat, f.lng)
            if address_result:
                food_dict['address'] = address_result['address']
        
        data.append(food_dict)
    
    return jsonify(data)