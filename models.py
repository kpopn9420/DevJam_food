from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

# 設定台灣時區
TW_TZ = pytz.timezone('Asia/Taipei')

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # provider or receiver
    rating = db.Column(db.Float, default=0.0)
    addr = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'rating': self.rating,
            'addr': self.addr,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Food(db.Model):
    __tablename__ = 'food_items'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)
    expire_time = db.Column(db.DateTime, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='available')  # available, reserved, done
    category = db.Column(db.String(50))  # e.g. "飲品", "肉類", "蔬菜"
    image_url = db.Column(db.String(500))  # Cloudinary or storage link
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 🔥 修復關係定義
    owner = db.relationship('User', backref=db.backref('foods', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'category': self.category,
            'lat': self.lat,
            'lng': self.lng,
            'expire_time': self.expire_time.isoformat() if self.expire_time else None,
            'image_url': self.image_url,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Reservation(db.Model):
    # 🔥 修復表名，改為複數形式
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='reserved')  # reserved, completed, expired, cancelled
    status = db.Column(db.String(20), default='reserved')  # reserved, completed, expired
    # 訂單成立時間
    reserve_time = db.Column(db.DateTime, default=datetime.utcnow)
    # 使用者預約時約定的取餐時間，如果需要固定時間取餐，可設定
    scheduled_pickup_time = db.Column(db.DateTime)
    # 實際取餐時間，用來檢核是否準時
    actual_pickup_time = db.Column(db.DateTime)
    # 取餐地點，可記錄當時 GPS
    pickup_lat = db.Column(db.Float)
    pickup_lng = db.Column(db.Float)
    # 取餐備註
    des = db.Column(db.String(250))
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔥 修復關係定義，指定正確的外鍵
    food = db.relationship('Food', backref=db.backref('reservations', lazy=True))
    owner = db.relationship('User', foreign_keys=[owner_id], backref=db.backref('owned_reservations', lazy=True))
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref=db.backref('received_reservations', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'food_id': self.food_id,
            'owner_id': self.owner_id,
            'receiver_id': self.receiver_id,
            'status': self.status,
            'reserve_time': self.reserve_time.isoformat() if self.reserve_time else None,
            'scheduled_pickup_time': self.scheduled_pickup_time.isoformat() if self.scheduled_pickup_time else None,
            'actual_pickup_time': self.actual_pickup_time.isoformat() if self.actual_pickup_time else None,
            'pickup_lat': self.pickup_lat,
            'pickup_lng': self.pickup_lng,
            'des': self.des,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 🔥 修復外鍵引用，使用正確的表名
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 1-5 分
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 🔥 修復關係定義
    from_user = db.relationship('User', foreign_keys=[from_user_id], backref=db.backref('given_ratings', lazy=True))
    to_user = db.relationship('User', foreign_keys=[to_user_id], backref=db.backref('received_ratings', lazy=True))
    reservation = db.relationship('Reservation', backref=db.backref('ratings', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'from_user_id': self.from_user_id,
            'to_user_id': self.to_user_id,
            'reservation_id': self.reservation_id,
            'score': self.score,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ESGLog(db.Model):
    __tablename__ = 'esg_logs'
    id = db.Column(db.Integer, primary_key=True)
    # 🔥 修復外鍵引用，使用正確的表名
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'), nullable=False)
    food_weight = db.Column(db.Float)  # in kg
    co2_saved = db.Column(db.Float)  # in kg CO2 saved
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 🔥 修復關係定義
    reservation = db.relationship('Reservation', backref=db.backref('esg_logs', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'reservation_id': self.reservation_id,
            'food_weight': self.food_weight,
            'co2_saved': self.co2_saved,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def drop_all_tables():
    """刪除所有表格"""
    db.drop_all()
    print("✅ 已刪除所有資料庫表格")

def reset_db():
    """重置資料庫"""
    drop_all_tables()
    init_db()
    print("✅ 資料庫重置完成")