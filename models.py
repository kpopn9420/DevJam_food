from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    owner = db.relationship('User', backref=db.backref('foods', lazy=True))

class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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

    food = db.relationship('Food', backref=db.backref('reservations', lazy=True))
    owner = db.relationship('User', foreign_keys=[owner_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resv_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # relationships omitted for brevity

class ESGLog(db.Model):
    __tablename__ = 'esg_logs'
    id = db.Column(db.Integer, primary_key=True)
    resv_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=False)
    food_weight = db.Column(db.Float)  # in kg
    co2 = db.Column(db.Float)  # in kg CO2 saved
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reservation = db.relationship('Reservation', backref=db.backref('esg_logs', lazy=True))
