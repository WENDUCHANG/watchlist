from flask import Blueprint
from flask import flash,redirect,url_for,request,render_template,make_response
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

        if not username or not password or len(username) > 10 or len(password) > 20:
            flash('非法登入输入（用户名最多10字符，密码最多20字符）')
            res = make_response(redirect(url_for('auth.login')))
            res.status = '303 Invalid login input redirect to login page'
            return res
            #return redirect(url_for('auth.login'))

        user = db.session.execute(select(User).filter_by(username=username)).scalar()
        # 验证密码是否一致
        if user is not None and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('登入成功')
            res = make_response(redirect(url_for('main.index')))
            res.status = '303 Login success redirect to home page'
            return res
            #return redirect(url_for('main.index'))  # 重定向到主页

        flash('错误的用户名或密码')  # 如果验证失败，显示错误消息
        res = make_response(redirect(url_for('auth.login')))
        res.status = '303 Invalid username or password redirect to login page'
        return res
        #return redirect(url_for('auth.login'))  # 重定向回登录页面

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('你已登出')

    res = make_response(redirect(url_for('main.index')))
    res.status = '307 Logout success redirect to home page'
    return res
    
    
    
    #return redirect(url_for('main.index')),307  # 重定向回首页