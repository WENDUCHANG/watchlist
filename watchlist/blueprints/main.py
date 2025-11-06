from flask import Blueprint
from flask import request,redirect,flash,url_for,render_template,make_response
from flask_login import login_required,current_user
from sqlalchemy import select

from watchlist.models import User,Movie
from watchlist.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('main.index'))
        title=request.form.get('title').strip()
        year = request.form.get('year').strip()
        if not title or not year or len(year)>4 or len(title)>60:
            flash('输入标题长度和年份不合法')
            res = make_response(redirect(url_for('main.index')))
            res.status = '301 invalid input redirect to home page'
            return res
            #return redirect(url_for('main.index'))
        #保存表单数据到数据库
        movie =Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('条目创建成功')
        res = make_response(redirect(url_for('main.index')))
        res.status = '302 Add success redirect to home page'
        return res
        #return redirect(url_for('main.index'))
    
    user = db.session.execute(select(User)).scalar()
    movies = db.session.execute(select(Movie)).scalars().all()
    #print(user.name)
    return render_template('index.html',movies=movies)

@main_bp.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = db.get_or_404(Movie, movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form.get('title').strip()
        year = request.form.get('year').strip()

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('main.edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('条目更改成功')
        res = make_response(redirect(url_for('main.index')))
        res.status = '302 edit success redirect to home page'
        return res
        #return redirect(url_for('main.index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录

@main_bp.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete(movie_id):
    movie = db.get_or_404(Movie, movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('条目已删除')
    res = make_response(redirect(url_for('main.index')))
    res.status = '302 delete success redirect to home page'
    return res
    #return redirect(url_for('main.index')),303  # 重定向回主页

@main_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form.get('name')

        if not name or len(name) > 20:
            flash('非法输入')
            return redirect(url_for('main.settings'))

        current_user.name = name  # 更新当前用户的名字
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = db.session.get(User, current_user.id)
        # user.name = name
        db.session.commit()
        flash('用户姓名已更改')
        res = make_response(redirect(url_for('main.index')))
        res.status = '302 setting success redirect to home page'
        return res
        #return redirect(url_for('main.index'))

    return render_template('settings.html')