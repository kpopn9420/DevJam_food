# init_db.py

from app import app
from models import db, Food, Reservation
from datetime import datetime


with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ 已刪除並重建所有資料表")