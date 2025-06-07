#!/usr/bin/env python3
"""Firebase 整合測試"""

def test_firebase_status():
    """測試 Firebase 連線狀態"""
    try:
        from firebase_config import get_firebase_status, FIREBASE_AVAILABLE
        status = get_firebase_status()
        print(f"Firebase 狀態: {status}")
        return FIREBASE_AVAILABLE
    except Exception as e:
        print(f"Firebase 錯誤: {e}")
        return False

def test_geo_service():
    """測試地理服務"""
    from geo_service import GeoService
    
    # 測試地址轉換
    result = GeoService.address_to_coordinates("台北101")
    print(f"地址轉換: {result}")
    
    # 測試附近搜尋
    if result:
        foods = GeoService.find_nearby_foods(result['lat'], result['lng'], 5)
        print(f"附近食物: {len(foods)} 個")

def test_food_sync():
    """測試食物同步"""
    firebase_available = test_firebase_status()
    
    if firebase_available:
        from firebase_food_service import FirebaseFoodService
        from models import Food
        
        # 取得 SQLite 食物
        foods = Food.query.limit(3).all()
        if foods:
            synced, errors, msg = FirebaseFoodService.sync_from_sqlite(foods)
            print(f"同步結果: {synced} 成功, {errors} 失敗")

if __name__ == '__main__':
    print("🔥 Firebase 整合測試")
    test_firebase_status()
    test_geo_service()
    test_food_sync()