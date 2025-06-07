# map_routes.py - 地圖功能相關路由

from flask import Blueprint, request, jsonify
from models import db, Food, User
from geo_service import GeoService
from firebase_food_service import FirebaseFoodService
import math
from datetime import datetime

map_bp = Blueprint('map', __name__)

@map_bp.route('/api/map/nearby_foods', methods=['GET'])
def get_nearby_foods_for_map():
    """取得地圖上附近的剩食 (增強版)"""
    try:
        # 取得查詢參數
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', default=5.0, type=float)  # 預設 5 公里
        category = request.args.get('category', default='', type=str)
        status = request.args.get('status', default='available', type=str)
        
        # 驗證必要參數
        if lat is None or lng is None:
            return jsonify({
                'status': 'error',
                'message': '缺少座標參數 (lat, lng)'
            }), 400
            
        # 驗證座標有效性 (台灣地區)
        if not GeoService.validate_coordinates(lat, lng):
            return jsonify({
                'status': 'error',
                'message': '座標無效或超出台灣地區範圍'
            }), 400
            
        # 限制搜尋半徑
        if radius > 50:
            radius = 50  # 最大 50 公里
        elif radius < 0.1:
            radius = 0.1  # 最小 100 公尺
            
        # 從 SQLite 取得基本資料
        query = Food.query.filter_by(status=status)
        
        # 如果有指定分類，加入篩選
        if category:
            query = query.filter_by(category=category)
            
        foods = query.all()
        
        # 計算距離並篩選
        nearby_foods = []
        for food in foods:
            # 檢查是否過期
            if food.expire_time < datetime.utcnow():
                continue
                
            # 計算距離
            distance = GeoService.calculate_distance(lat, lng, food.lat, food.lng)
            
            if distance <= radius:
                # 取得擁有者資訊
                owner = User.query.get(food.owner_id)
                
                food_data = {
                    'id': food.id,
                    'name': food.name,
                    'description': food.description,
                    'quantity': food.quantity,
                    'category': food.category,
                    'lat': food.lat,
                    'lng': food.lng,
                    'distance': round(distance, 2),
                    'expire_time': food.expire_time.isoformat(),
                    'image_url': food.image_url,
                    'status': food.status,
                    'created_at': food.created_at.isoformat(),
                    'owner': {
                        'id': owner.id if owner else None,
                        'name': owner.name if owner else '未知',
                        'rating': owner.rating if owner else 0.0
                    }
                }
                nearby_foods.append(food_data)
        
        # 按距離排序
        nearby_foods.sort(key=lambda x: x['distance'])
        
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
        return jsonify({
            'status': 'error',
            'message': f'搜尋附近剩食失敗: {str(e)}'
        }), 500

@map_bp.route('/api/map/food_clusters', methods=['GET'])
def get_food_clusters():
    """取得地圖上的食物聚集點資訊"""
    try:
        # 取得查詢參數
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        zoom = request.args.get('zoom', default=12, type=int)
        
        if lat is None or lng is None:
            return jsonify({
                'status': 'error',
                'message': '缺少座標參數'
            }), 400
            
        # 根據縮放等級決定聚集範圍
        cluster_radius = 2.0 if zoom >= 15 else 5.0 if zoom >= 12 else 10.0
        
        foods = Food.query.filter_by(status='available').all()
        clusters = []
        processed_foods = set()
        
        for food in foods:
            if food.id in processed_foods:
                continue
                
            # 找出這個點附近的其他食物
            cluster_foods = [food]
            cluster_center_lat = food.lat
            cluster_center_lng = food.lng
            
            for other_food in foods:
                if (other_food.id != food.id and 
                    other_food.id not in processed_foods):
                    
                    distance = GeoService.calculate_distance(
                        food.lat, food.lng,
                        other_food.lat, other_food.lng
                    )
                    
                    if distance <= cluster_radius:
                        cluster_foods.append(other_food)
                        
            # 計算聚集點中心
            if len(cluster_foods) > 1:
                total_lat = sum(f.lat for f in cluster_foods)
                total_lng = sum(f.lng for f in cluster_foods)
                cluster_center_lat = total_lat / len(cluster_foods)
                cluster_center_lng = total_lng / len(cluster_foods)
            
            # 標記已處理的食物
            for f in cluster_foods:
                processed_foods.add(f.id)
                
            # 建立聚集點資料
            cluster = {
                'center': {
                    'lat': cluster_center_lat,
                    'lng': cluster_center_lng
                },
                'count': len(cluster_foods),
                'foods': [
                    {
                        'id': f.id,
                        'name': f.name,
                        'category': f.category,
                        'lat': f.lat,
                        'lng': f.lng,
                        'expire_time': f.expire_time.isoformat(),
                        'image_url': f.image_url
                    }
                    for f in cluster_foods
                ]
            }
            clusters.append(cluster)
            
        return jsonify({
            'status': 'success',
            'data': {
                'zoom_level': zoom,
                'cluster_radius': cluster_radius,
                'total_clusters': len(clusters),
                'clusters': clusters
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'取得聚集點失敗: {str(e)}'
        }), 500

@map_bp.route('/api/map/area_stats', methods=['GET'])
def get_area_statistics():
    """取得指定區域的統計資訊"""
    try:
        # 取得查詢參數
        north = request.args.get('north', type=float)
        south = request.args.get('south', type=float)
        east = request.args.get('east', type=float)
        west = request.args.get('west', type=float)
        
        if not all([north, south, east, west]):
            return jsonify({
                'status': 'error',
                'message': '缺少邊界參數 (north, south, east, west)'
            }), 400
            
        # 查詢區域內的食物
        foods_in_area = Food.query.filter(
            Food.lat >= south,
            Food.lat <= north,
            Food.lng >= west,
            Food.lng <= east,
            Food.status == 'available'
        ).all()
        
        # 統計分析
        total_count = len(foods_in_area)
        category_stats = {}
        
        for food in foods_in_area:
            category = food.category or '其他'
            if category not in category_stats:
                category_stats[category] = 0
            category_stats[category] += 1
            
        # 計算即將到期的食物數量 (24小時內)
        now = datetime.utcnow()
        expiring_soon = sum(1 for food in foods_in_area 
                          if (food.expire_time - now).total_seconds() <= 86400)
        
        return jsonify({
            'status': 'success',
            'data': {
                'area_bounds': {
                    'north': north,
                    'south': south,
                    'east': east,
                    'west': west
                },
                'total_available_foods': total_count,
                'expiring_soon_count': expiring_soon,
                'category_distribution': category_stats,
                'density_per_km2': round(total_count / ((north - south) * (east - west) * 12321), 2)  # 概略計算
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'取得區域統計失敗: {str(e)}'
        }), 500

@map_bp.route('/api/map/heatmap_data', methods=['GET'])
def get_heatmap_data():
    """取得熱力圖資料"""
    try:
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', default=10.0, type=float)
        
        if lat is None or lng is None:
            return jsonify({
                'status': 'error',
                'message': '缺少中心座標'
            }), 400
            
        # 取得範圍內的所有食物
        lat_range = radius / 111.0
        lng_range = radius / (111.0 * math.cos(math.radians(lat)))
        
        foods = Food.query.filter(
            Food.lat >= lat - lat_range,
            Food.lat <= lat + lat_range,
            Food.lng >= lng - lng_range,
            Food.lng <= lng + lng_range,
            Food.status == 'available'
        ).all()
        
        # 建立熱力圖資料點
        heatmap_points = []
        for food in foods:
            # 計算權重 (基於數量和即將到期程度)
            time_to_expire = (food.expire_time - datetime.utcnow()).total_seconds()
            urgency_weight = max(0.1, min(1.0, 86400 / max(3600, time_to_expire)))  # 1-24小時權重較高
            
            weight = food.quantity * urgency_weight
            
            heatmap_points.append({
                'lat': food.lat,
                'lng': food.lng,
                'weight': weight,
                'food_id': food.id,
                'name': food.name,
                'category': food.category
            })
            
        return jsonify({
            'status': 'success',
            'data': {
                'center': {'lat': lat, 'lng': lng},
                'radius': radius,
                'points': heatmap_points,
                'max_weight': max([p['weight'] for p in heatmap_points]) if heatmap_points else 0
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'取得熱力圖資料失敗: {str(e)}'
        }), 500

# Firebase 同步功能
@map_bp.route('/api/map/sync_to_firebase', methods=['POST'])
def sync_foods_to_firebase():
    """將 SQLite 的食物資料同步到 Firebase (用於地圖快取)"""
    try:
        data = request.get_json() or {}
        force_sync = data.get('force', False)
        
        # 取得所有可用的食物
        foods = Food.query.filter_by(status='available').all()
        
        synced_count = 0
        error_count = 0
        
        for food in foods:
            # 準備 Firebase 資料
            firebase_data = {
                'id': food.id,
                'name': food.name,
                'description': food.description,
                'quantity': food.quantity,
                'category': food.category,
                'lat': food.lat,
                'lng': food.lng,
                'status': food.status,
                'expire_time': food.expire_time.isoformat(),
                'image_url': food.image_url,
                'owner_id': food.owner_id,
                'created_at': food.created_at.isoformat()
            }
            
            # 同步到 Firebase
            doc_id, error = FirebaseFoodService.create_food(firebase_data)
            
            if error:
                error_count += 1
                if not force_sync:
                    print(f"同步食物 {food.id} 失敗: {error}")
            else:
                synced_count += 1
                
        return jsonify({
            'status': 'success',
            'message': f'同步完成: {synced_count} 成功, {error_count} 失敗',
            'synced_count': synced_count,
            'error_count': error_count
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'同步失敗: {str(e)}'
        }), 500

# CORS 處理
@map_bp.route('/api/map/nearby_foods', methods=['OPTIONS'])
@map_bp.route('/api/map/food_clusters', methods=['OPTIONS'])
@map_bp.route('/api/map/area_stats', methods=['OPTIONS'])
@map_bp.route('/api/map/heatmap_data', methods=['OPTIONS'])
@map_bp.route('/api/map/sync_to_firebase', methods=['OPTIONS'])
def handle_map_options():
    """處理地圖相關路由的 CORS preflight 請求"""
    response = jsonify()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response