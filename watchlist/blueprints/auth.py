from flask import Blueprint
from flask import flash,redirect,url_for,request,render_template
from sqlalchemy import select
from flask_login import login_user,login_required,logout_user
from watchlist.models import User
from watchlist.extensions import db

auth_bp=Blueprint('auth',__name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('非法输入')
            return redirect(url_for('auth.login'))

        user = db.session.execute(select(User).filter_by(username=username)).scalar()
        # 验证密码是否一致
        if user is not None and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('登入成功')
            return redirect(url_for('main.index'))  # 重定向到主页

        flash('错误的用户名或密码')  # 如果验证失败，显示错误消息
        return redirect(url_for('auth.login'))  # 重定向回登录页面

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('你已登出')
    return redirect(url_for('main.index'))  # 重定向回首页