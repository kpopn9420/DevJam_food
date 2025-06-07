from flask import Blueprint, request, jsonify
from models import db, Food, User
from geo_service import GeoService
from datetime import datetime

map_bp = Blueprint('map', __name__)

@map_bp.route('/api/map/nearby_foods', methods=['GET'])
def get_nearby_foods_for_map():
    """取得地圖上附近的剩食"""
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', default=5.0, type=float)
        category = request.args.get('category', default='', type=str)
        status = request.args.get('status', default='available', type=str)
        
        if lat is None or lng is None:
            return jsonify({'status': 'error', 'message': '缺少座標參數'}), 400
            
        if not GeoService.validate_coordinates(lat, lng):
            return jsonify({'status': 'error', 'message': '座標無效'}), 400
            
        radius = min(max(radius, 0.1), 50)  # 限制範圍
        
        # 使用整合的 GeoService 搜尋
        nearby_foods = GeoService.find_nearby_foods(lat, lng, radius)
        
        # 如果有分類篩選
        if category:
            nearby_foods = [f for f in nearby_foods if f.get('category') == category]
        
        # 添加擁有者資訊
        for food in nearby_foods:
            owner = User.query.get(food.get('owner_id'))
            food['owner'] = {
                'id': owner.id if owner else None,
                'name': owner.name if owner else '未知',
                'rating': owner.rating if owner else 0.0
            } if owner else None
        
        return jsonify({
            'status': 'success',
            'data': {
                'search_center': {'lat': lat, 'lng': lng},
                'search_radius': radius,
                'total_count': len(nearby_foods),
                'foods': nearby_foods
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@map_bp.route('/api/map/area_stats', methods=['GET'])
def get_area_statistics():
    """取得指定區域的統計資訊"""
    try:
        north = request.args.get('north', type=float)
        south = request.args.get('south', type=float)
        east = request.args.get('east', type=float)
        west = request.args.get('west', type=float)
        
        if not all([north, south, east, west]):
            return jsonify({'status': 'error', 'message': '缺少邊界參數'}), 400
            
        foods_in_area = Food.query.filter(
            Food.lat >= south, Food.lat <= north,
            Food.lng >= west, Food.lng <= east,
            Food.status == 'available'
        ).all()
        
        total_count = len(foods_in_area)
        category_stats = {}
        
        for food in foods_in_area:
            category = food.category or '其他'
            category_stats[category] = category_stats.get(category, 0) + 1
            
        now = datetime.utcnow()
        expiring_soon = sum(1 for food in foods_in_area 
                          if (food.expire_time - now).total_seconds() <= 86400)
        
        return jsonify({
            'status': 'success',
            'data': {
                'area_bounds': {'north': north, 'south': south, 'east': east, 'west': west},
                'total_available_foods': total_count,
                'expiring_soon_count': expiring_soon,
                'category_distribution': category_stats,
                'density_per_km2': round(total_count / ((north - south) * (east - west) * 12321), 2)
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# CORS 處理
@map_bp.route('/api/map/<path:endpoint>', methods=['OPTIONS'])
def handle_map_options(endpoint):
    response = jsonify()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response