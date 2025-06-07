# app.py

from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from models import db
from routes.food_routes import food_bp
from routes.reservation_routes import reservation_bp

app = Flask(__name__)
CORS(app)


SWAGGER_URL = '/docs'                # 你要瀏覽的路徑
API_URL     = '/static/openapi.yaml' # swagger 要讀的 OpenAPI 規格檔

swagger_bp = get_swaggerui_blueprint(
    '/docs',
    '/static/openapi.yaml',
    config={'app_name': "FoodShare API"}
)
app.register_blueprint(swagger_bp, url_prefix='/docs')
# 本機 MySQL 設定（依照你自己的設定修改）
# app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/foodsystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(food_bp)
app.register_blueprint(reservation_bp)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return '後端 B 啟動成功！'

if __name__ == '__main__':
    app.run(debug=True)
