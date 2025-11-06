from flask import Flask
from sqlalchemy import select

from watchlist.extensions import db, login_manager
from watchlist.blueprints.main import main_bp
from watchlist.blueprints.auth import auth_bp
from watchlist.models import User
from watchlist.errors import register_errors, register_static_status
from watchlist.commands import register_commands
from watchlist.settings import config

def create_app(config_name='development'):
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(config[config_name])

    #注册蓝本
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    #初始化拓展
    db.init_app(app)
    login_manager.init_app(app)

    #注册错误处理函数和命令
    register_errors(app)
    register_commands(app)
    register_static_status(app, 305)  # 将静态文件状态设为 201（或改为你需要的整数）

    @app.context_processor
    def inject_user():
        user = db.session.execute(select(User)).scalar()
        return dict(user=user)
    
    return app