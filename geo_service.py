import math
from datetime import datetime

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

    @staticmethod
    def find_nearby_foods(user_lat, user_lng, radius_km=5):
        """找尋附近的食物"""
        if not FIREBASE_AVAILABLE:
            return []
        
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
            print(f"地理查詢錯誤: {str(e)}")
            return []