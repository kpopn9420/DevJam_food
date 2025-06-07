from app import app
from models import db, User, Food, Reservation, Rating, ESGLog
from datetime import datetime, timedelta
import hashlib

def hash_password(password):
    """簡單的密碼雜湊函式"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_sample_data():
    """建立範例資料"""
    try:
        # 建立範例用戶
        users = [
            User(
                email='alice@example.com',
                password_hash=hash_password('password123'),
                name='Alice Chen',
                role='provider',
                rating=4.5,
                addr='台北市大安區'
            ),
            User(
                email='bob@example.com',
                password_hash=hash_password('password123'),
                name='Bob Lin',
                role='receiver',
                rating=4.2,
                addr='台北市信義區'
            ),
            User(
                email='carol@example.com',
                password_hash=hash_password('password123'),
                name='Carol Wu',
                role='provider',
                rating=4.8,
                addr='台北市中山區'
            )
        ]
        
        for user in users:
            db.session.add(user)
        db.session.commit()
        print("✅ 已建立範例用戶")
        
        # 建立範例食物
        foods = [
            Food(
                owner_id=1,  # Alice
                name='新鮮麵包',
                description='剛出爐的吐司麵包，有兩條',
                quantity=2,
                expire_time=datetime.utcnow() + timedelta(days=2),
                lat=25.0330,
                lng=121.5654,
                status='available',
                category='麵包',
                image_url='https://example.com/bread.jpg'
            ),
            Food(
                owner_id=3,  # Carol
                name='蘋果',
                description='新鮮蘋果，約10顆',
                quantity=10,
                expire_time=datetime.utcnow() + timedelta(days=5),
                lat=25.0521,
                lng=121.5654,
                status='available',
                category='水果',
                image_url='https://example.com/apple.jpg'
            ),
            Food(
                owner_id=1,  # Alice
                name='便當',
                description='排骨便當，今天做的',
                quantity=3,
                expire_time=datetime.utcnow() + timedelta(hours=12),
                lat=25.0330,
                lng=121.5654,
                status='reserved',  # 已被預約
                category='便當',
                image_url='https://example.com/bento.jpg'
            )
        ]
        
        for food in foods:
            db.session.add(food)
        db.session.commit()
        print("✅ 已建立範例食物")
        
        # 建立範例預約
        reservation = Reservation(
            food_id=3,  # 便當
            owner_id=1,  # Alice
            receiver_id=2,  # Bob
            status='reserved',
            reserve_time=datetime.utcnow(),
            scheduled_pickup_time=datetime.utcnow() + timedelta(hours=2)
        )
        
        db.session.add(reservation)
        db.session.commit()
        print("✅ 已建立範例預約")
        
        # 建立範例評分
        rating = Rating(
            from_user_id=2,  # Bob 評價 Alice
            to_user_id=1,
            reservation_id=1,
            score=5,
            comment='食物很新鮮，取餐過程很順利！'
        )
        
        db.session.add(rating)
        db.session.commit()
        print("✅ 已建立範例評分")
        
        # 建立範例 ESG 記錄
        esg_log = ESGLog(
            reservation_id=1,
            food_weight=0.5,  # 0.5 kg
            co2_saved=1.2,   # 節省 1.2 kg CO2
            category='便當'
        )
        
        db.session.add(esg_log)
        db.session.commit()
        print("✅ 已建立範例 ESG 記錄")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ 建立範例資料時發生錯誤: {str(e)}")

def main():
    """主要執行函式"""
    with app.app_context():
        try:
            # 刪除所有現有表格
            db.drop_all()
            print("✅ 已刪除所有現有表格")
            
            # 重新建立所有表格
            db.create_all()
            print("✅ 已重新建立所有表格")
            
            # 檢查表格是否建立成功
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✅ 建立的表格: {', '.join(tables)}")
            
            # 建立範例資料
            print("\n🔄 開始建立範例資料...")
            create_sample_data()
            
            print("\n🎉 資料庫初始化完成！")
            print("\n📊 範例資料摘要:")
            print(f"用戶數量: {User.query.count()}")
            print(f"食物數量: {Food.query.count()}")
            print(f"預約數量: {Reservation.query.count()}")
            print(f"評分數量: {Rating.query.count()}")
            print(f"ESG記錄數量: {ESGLog.query.count()}")
            
        except Exception as e:
            print(f"❌ 資料庫初始化失敗: {str(e)}")
            raise

if __name__ == '__main__':
    main()