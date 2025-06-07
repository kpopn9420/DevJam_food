from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# 嘗試導入 Firebase，如果失敗則設為不可用
try:
    from firebase_config import db, FIREBASE_AVAILABLE
    if not FIREBASE_AVAILABLE or db is None:
        logger.warning("Firebase 不可用，將使用 SQLite fallback")
        FIREBASE_AVAILABLE = False
except ImportError as e:
    logger.warning(f"無法導入 Firebase: {e}")
    FIREBASE_AVAILABLE = False
    db = None

class FirebaseFoodService:
    @staticmethod
    def create_food(food_data):
        """在 Firestore 建立食物記錄"""
        if not FIREBASE_AVAILABLE or db is None:
            logger.info("Firebase 未啟用，跳過 Firestore 操作")
            return None, "Firebase 未啟用"
        
        try:
            food_data['created_at'] = datetime.utcnow()
            food_data['updated_at'] = datetime.utcnow()
            
            doc_ref = db.collection('foods').document()
            doc_ref.set(food_data)
            
            logger.info(f"成功在 Firestore 建立食物記錄: {doc_ref.id}")
            return doc_ref.id, None
        except Exception as e:
            logger.error(f"Firestore 建立食物失敗: {str(e)}")
            return None, str(e)

    @staticmethod
    def update_food_status(food_id, status, additional_data=None):
        """更新食物狀態"""
        if not FIREBASE_AVAILABLE or db is None:
            logger.info("Firebase 未啟用，跳過狀態更新")
            return False, "Firebase 未啟用"
        
        try:
            doc_ref = db.collection('foods').document(food_id)
            
            update_data = {
                'status': status,
                'updated_at': datetime.utcnow()
            }
            
            if additional_data:
                update_data.update(additional_data)
            
            doc_ref.update(update_data)
            logger.info(f"成功更新 Firestore 食物狀態: {food_id} -> {status}")
            return True, None
        except Exception as e:
            logger.error(f"Firestore 更新狀態失敗: {str(e)}")
            return False, str(e)

    @staticmethod
    def get_user_foods(user_id):
        """取得用戶發布的食物"""
        if not FIREBASE_AVAILABLE or db is None:
            logger.info("Firebase 未啟用，返回空列表")
            return [], "Firebase 未啟用"
        
        try:
            foods_ref = db.collection('foods')
            docs = foods_ref.where('owner_id', '==', user_id)\
                           .order_by('created_at', direction='DESCENDING')\
                           .get()
            
            foods = []
            for doc in docs:
                food_data = doc.to_dict()
                food_data['id'] = doc.id
                foods.append(food_data)
            
            logger.info(f"從 Firestore 取得 {len(foods)} 筆用戶食物")
            return foods, None
        except Exception as e:
            logger.error(f"Firestore 查詢用戶食物失敗: {str(e)}")
            return [], str(e)

    @staticmethod
    def delete_food(food_id, user_id):
        """刪除食物"""
        if not FIREBASE_AVAILABLE or db is None:
            logger.info("Firebase 未啟用，跳過刪除操作")
            return False, "Firebase 未啟用"
        
        try:
            doc_ref = db.collection('foods').document(food_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                return False, "食物不存在"
            
            food_data = doc.to_dict()
            if food_data.get('owner_id') != user_id:
                return False, "無權限刪除此食物"
            
            doc_ref.delete()
            logger.info(f"成功從 Firestore 刪除食物: {food_id}")
            return True, None
        except Exception as e:
            logger.error(f"Firestore 刪除食物失敗: {str(e)}")
            return False, str(e)

    @staticmethod
    def sync_from_sqlite(sqlite_foods):
        """從 SQLite 同步食物到 Firestore"""
        if not FIREBASE_AVAILABLE or db is None:
            return 0, len(sqlite_foods), "Firebase 未啟用"
        
        synced_count = 0
        error_count = 0
        
        for food in sqlite_foods:
            try:
                # 準備 Firestore 資料
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
                    'created_at': food.created_at.isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
                
                # 使用 SQLite ID 作為 Firestore 文檔 ID
                doc_ref = db.collection('foods').document(str(food.id))
                doc_ref.set(firebase_data, merge=True)
                synced_count += 1
                
            except Exception as e:
                logger.error(f"同步食物 {food.id} 失敗: {str(e)}")
                error_count += 1
                
        logger.info(f"同步完成: {synced_count} 成功, {error_count} 失敗")
        return synced_count, error_count, None

    @staticmethod
    def is_available():
        """檢查 Firebase 是否可用"""
        return FIREBASE_AVAILABLE and db is not None

    @staticmethod
    def get_status():
        """取得 Firebase 服務狀態"""
        return {
            'firebase_available': FIREBASE_AVAILABLE,
            'firestore_connected': db is not None,
            'service_name': 'FirebaseFoodService'
        }