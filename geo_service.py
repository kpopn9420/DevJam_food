import math
import requests
import re
from datetime import datetime
from urllib.parse import quote

# Firebase 整合
try:
    from firebase_config import db
    FIREBASE_AVAILABLE = db is not None
except ImportError:
    FIREBASE_AVAILABLE = False

class GeoService:
    @staticmethod
    def calculate_distance(lat1, lng1, lat2, lng2):
        """計算兩點間距離（公里）- Haversine 公式"""
        R = 6371  # 地球半徑（公里）
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lng/2) * math.sin(delta_lng/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    @staticmethod
    def validate_coordinates(lat, lng):
        """驗證座標有效性（台灣地區）"""
        if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
            return False
        
        # 台灣地區座標範圍
        if not (21.5 <= lat <= 25.5):  # 台灣緯度範圍
            return False
        if not (119.5 <= lng <= 122.5):  # 台灣經度範圍
            return False
            
        return True

    # === 地址轉換功能 ===
    @staticmethod
    def address_to_coordinates(address):
        """地址轉經緯度 - 優先使用 Firebase，備援免費服務"""
        clean_address = GeoService._clean_address(address)
        
        # 嘗試多個服務
        services = [
            GeoService._nominatim_geocode,
            GeoService._opencage_geocode,
            GeoService._mapbox_geocode
        ]
        
        for service in services:
            try:
                result = service(clean_address)
                if result:
                    # 如果 Firebase 可用，同時儲存到快取
                    if FIREBASE_AVAILABLE:
                        GeoService._cache_geocode_result(address, result)
                    return result
            except Exception as e:
                print(f"地理編碼服務錯誤: {e}")
                continue
        
        return None

    @staticmethod
    def _clean_address(address):
        """清理和標準化地址"""
        if not address:
            return ""
        
        # 展開台灣地址縮寫
        address_mapping = {
            '北市': '台北市', '新北': '新北市', '桃市': '桃園市',
            '台中': '台中市', '台南': '台南市', '高市': '高雄市'
        }
        
        for short, full in address_mapping.items():
            address = address.replace(short, full)
        
        # 移除多餘空白
        address = re.sub(r'\s+', ' ', address.strip())
        
        # 如果沒有包含台灣，自動添加
        if '台灣' not in address and 'Taiwan' not in address:
            address = f"台灣 {address}"
        
        return address

    @staticmethod
    def _nominatim_geocode(address):
        """使用 Nominatim (OpenStreetMap) 服務"""
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'limit': 1,
            'countrycodes': 'tw',
            'addressdetails': 1
        }
        
        headers = {
            'User-Agent': 'FoodShareApp/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lng = float(data[0]['lon'])
                
                if GeoService.validate_coordinates(lat, lng):
                    return {
                        'lat': lat,
                        'lng': lng,
                        'formatted_address': data[0].get('display_name', address),
                        'service': 'nominatim'
                    }
        
        return None

    @staticmethod
    def _opencage_geocode(address):
        """使用 OpenCage 服務 (可選)"""
        import os
        api_key = os.getenv('OPENCAGE_API_KEY')
        if not api_key:
            return None
        
        url = "https://api.opencagedata.com/geocode/v1/json"
        params = {
            'q': address,
            'key': api_key,
            'limit': 1,
            'countrycode': 'tw',
            'language': 'zh-TW'
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                result = data['results'][0]
                lat = result['geometry']['lat']
                lng = result['geometry']['lng']
                
                if GeoService.validate_coordinates(lat, lng):
                    return {
                        'lat': lat,
                        'lng': lng,
                        'formatted_address': result['formatted'],
                        'service': 'opencage'
                    }
        
        return None

    @staticmethod
    def _mapbox_geocode(address):
        """使用 Mapbox 服務 (可選)"""
        import os
        api_key = os.getenv('MAPBOX_API_KEY')
        if not api_key:
            return None
        
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{quote(address)}.json"
        params = {
            'access_token': api_key,
            'limit': 1,
            'country': 'tw',
            'language': 'zh-TW'
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data['features']:
                feature = data['features'][0]
                lng, lat = feature['geometry']['coordinates']
                
                if GeoService.validate_coordinates(lat, lng):
                    return {
                        'lat': lat,
                        'lng': lng,
                        'formatted_address': feature['place_name'],
                        'service': 'mapbox'
                    }
        
        return None

    @staticmethod
    def coordinates_to_address(lat, lng):
        """反向地理編碼：經緯度轉地址"""
        if not GeoService.validate_coordinates(lat, lng):
            return None
        
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': lat,
            'lon': lng,
            'format': 'json',
            'addressdetails': 1,
            'accept-language': 'zh-TW,zh,en'
        }
        
        headers = {
            'User-Agent': 'FoodShareApp/1.0'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'display_name' in data:
                    result = {
                        'address': data['display_name'],
                        'details': data.get('address', {}),
                        'service': 'nominatim'
                    }
                    
                    # 如果 Firebase 可用，儲存結果
                    if FIREBASE_AVAILABLE:
                        GeoService._cache_reverse_geocode_result(lat, lng, result)
                    
                    return result
        except Exception as e:
            print(f"反向地理編碼錯誤: {e}")
        
        return None

    # === Firebase 快取功能 ===
    @staticmethod
    def _cache_geocode_result(address, result):
        """將地理編碼結果快取到 Firebase"""
        if not FIREBASE_AVAILABLE:
            return
        
        try:
            cache_data = {
                'address': address,
                'lat': result['lat'],
                'lng': result['lng'],
                'formatted_address': result['formatted_address'],
                'service': result['service'],
                'cached_at': datetime.utcnow(),
                'type': 'forward'
            }
            
            # 使用地址作為文檔 ID (經過清理)
            doc_id = re.sub(r'[^\w\u4e00-\u9fff]', '_', address)
            db.collection('geocode_cache').document(doc_id).set(cache_data)
            
        except Exception as e:
            print(f"快取地理編碼結果失敗: {e}")

    @staticmethod
    def _cache_reverse_geocode_result(lat, lng, result):
        """將反向地理編碼結果快取到 Firebase"""
        if not FIREBASE_AVAILABLE:
            return
        
        try:
            cache_data = {
                'lat': lat,
                'lng': lng,
                'address': result['address'],
                'details': result['details'],
                'service': result['service'],
                'cached_at': datetime.utcnow(),
                'type': 'reverse'
            }
            
            # 使用座標作為文檔 ID
            doc_id = f"{lat:.6f}_{lng:.6f}".replace('.', '_')
            db.collection('geocode_cache').document(doc_id).set(cache_data)
            
        except Exception as e:
            print(f"快取反向地理編碼結果失敗: {e}")

    # === Firebase 增強的附近食物搜尋 ===
    @staticmethod
    def find_nearby_foods(user_lat, user_lng, radius_km=5):
        """找尋附近的食物 - Firebase 優先，SQLite 備援"""
        if FIREBASE_AVAILABLE:
            return GeoService._find_nearby_foods_firebase(user_lat, user_lng, radius_km)
        else:
            return GeoService._find_nearby_foods_sqlite(user_lat, user_lng, radius_km)

    @staticmethod
    def _find_nearby_foods_firebase(user_lat, user_lng, radius_km):
        """使用 Firebase 搜尋附近食物"""
        try:
            # 計算搜尋邊界
            lat_range = radius_km / 111.0
            lng_range = radius_km / (111.0 * math.cos(math.radians(user_lat)))
            
            # Firestore 查詢
            foods_ref = db.collection('foods')
            foods = foods_ref.where('status', '==', 'available')\
                             .where('lat', '>=', user_lat - lat_range)\
                             .where('lat', '<=', user_lat + lat_range)\
                             .get()
            
            # 客戶端篩選經度和精確距離
            nearby_foods = []
            for food_doc in foods:
                food_data = food_doc.to_dict()
                food_data['id'] = food_doc.id
                
                # 檢查經度範圍
                if (food_data['lng'] < user_lng - lng_range or 
                    food_data['lng'] > user_lng + lng_range):
                    continue
                
                # 計算精確距離
                distance = GeoService.calculate_distance(
                    user_lat, user_lng,
                    food_data['lat'], food_data['lng']
                )
                
                if distance <= radius_km:
                    food_data['distance'] = round(distance, 2)
                    nearby_foods.append(food_data)
            
            return sorted(nearby_foods, key=lambda x: x['distance'])
            
        except Exception as e:
            print(f"Firebase 地理查詢錯誤: {str(e)}")
            return []

    @staticmethod
    def _find_nearby_foods_sqlite(user_lat, user_lng, radius_km):
        """使用 SQLite 搜尋附近食物 (備援)"""
        try:
            from models import Food
            
            foods = Food.query.filter_by(status='available').all()
            nearby_foods = []
            
            for food in foods:
                distance = GeoService.calculate_distance(
                    user_lat, user_lng, food.lat, food.lng
                )
                
                if distance <= radius_km:
                    food_data = food.to_dict()
                    food_data['distance'] = round(distance, 2)
                    nearby_foods.append(food_data)
            
            return sorted(nearby_foods, key=lambda x: x['distance'])
            
        except Exception as e:
            print(f"SQLite 地理查詢錯誤: {str(e)}")
            return []

    # === 批量處理功能 ===
    @staticmethod
    def batch_geocode(addresses):
        """批量地址轉換"""
        results = []
        for i, address in enumerate(addresses):
            if not address or not address.strip():
                results.append({
                    'index': i,
                    'address': address,
                    'status': 'error',
                    'message': '地址為空'
                })
                continue
            
            result = GeoService.address_to_coordinates(address.strip())
            
            if result:
                results.append({
                    'index': i,
                    'address': address,
                    'status': 'success',
                    'coordinates': {
                        'lat': result['lat'],
                        'lng': result['lng']
                    },
                    'formatted_address': result['formatted_address']
                })
            else:
                results.append({
                    'index': i,
                    'address': address,
                    'status': 'error',
                    'message': '無法找到座標'
                })
        
        return results