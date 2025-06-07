import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 全域變數
db = None
bucket = None
FIREBASE_AVAILABLE = False

def initialize_firebase():
    """初始化 Firebase - 加強錯誤處理"""
    global db, bucket, FIREBASE_AVAILABLE
    
    # 如果已經初始化過且成功，直接返回
    if FIREBASE_AVAILABLE and db is not None:
        return db
        
    try:
        if not firebase_admin._apps:
            cred = None
            
            # 方法 1: 嘗試使用服務帳戶金鑰檔案
            service_key_path = 'service-account-key.json'
            if os.path.exists(service_key_path):
                logger.info("使用服務帳戶金鑰檔案初始化 Firebase")
                cred = credentials.Certificate(service_key_path)
            else:
                logger.warning(f"找不到服務帳戶金鑰檔案: {service_key_path}")
                
                # 方法 2: 嘗試使用環境變數
                if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
                    logger.info("使用環境變數 GOOGLE_APPLICATION_CREDENTIALS")
                    cred = credentials.ApplicationDefault()
                else:
                    logger.warning("未設定 GOOGLE_APPLICATION_CREDENTIALS 環境變數")
                    
                    # 方法 3: 嘗試其他可能的路徑
                    possible_paths = [
                        './credentials/service-account-key.json',
                        '../service-account-key.json',
                        os.path.expanduser('~/service-account-key.json')
                    ]
                    
                    for path in possible_paths:
                        if os.path.exists(path):
                            logger.info(f"在 {path} 找到服務帳戶金鑰")
                            cred = credentials.Certificate(path)
                            break
            
            if cred is None:
                logger.error("⚠️  無法找到 Firebase 認證檔案")
                logger.info("📝 請執行以下步驟來設定 Firebase:")
                logger.info("1. 到 Firebase Console > 專案設定 > 服務帳戶")
                logger.info("2. 點擊「產生新的私密金鑰」")
                logger.info("3. 將下載的 JSON 檔案重新命名為 'service-account-key.json'")
                logger.info("4. 將檔案放在與 app.py 相同的目錄下")
                logger.info("5. 或設定環境變數: export GOOGLE_APPLICATION_CREDENTIALS='path/to/your/key.json'")
                return None
                
            # 取得專案 ID (從環境變數或認證檔案)
            project_id = os.getenv('FIREBASE_PROJECT_ID', 'your-project-id')
            storage_bucket = f"{project_id}.appspot.com"
            
            # 初始化 Firebase
            firebase_admin.initialize_app(cred, {
                'storageBucket': storage_bucket
            })
            
            logger.info("✅ Firebase 初始化成功")
        
        # 取得 Firestore 和 Storage 客戶端
        db = firestore.client()
        bucket = storage.bucket()
        FIREBASE_AVAILABLE = True
        
        logger.info("✅ Firestore 和 Storage 客戶端建立成功")
        return db
        
    except Exception as e:
        logger.error(f"❌ Firebase 初始化失敗: {str(e)}")
        logger.info("🔄 應用程式將以 SQLite-only 模式運行")
        FIREBASE_AVAILABLE = False
        db = None
        bucket = None
        return None

def get_firebase_status():
    """取得 Firebase 連線狀態"""
    return {
        'available': FIREBASE_AVAILABLE,
        'firestore': db is not None,
        'storage': bucket is not None,
        'error': None if FIREBASE_AVAILABLE else "Firebase 未正確初始化"
    }

# 嘗試初始化 Firebase
try:
    db = initialize_firebase()
except Exception as e:
    logger.warning(f"Firebase 自動初始化失敗: {str(e)}")
    db = None

# 導出變數供其他模組使用
__all__ = ['db', 'bucket', 'FIREBASE_AVAILABLE', 'initialize_firebase', 'get_firebase_status']