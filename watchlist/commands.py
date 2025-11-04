from sqlalchemy import select
import click
from watchlist.extensions import db
from watchlist.models import User,Movie
#from app import app

def register_commands(app):
    @app.cli.command('init-db')
    @click.option('--drop', is_flag=True, help='Crete after drop.')
    def init_database(drop):
        if drop:
            db.drop_all()
            db.create_all
        click.echo('Initialized database.')
    @app.cli.command()
    def forge():
        """Generate fake data."""
        db.drop_all()
        db.create_all()
        # 全局的两个变量移动到这个函数内
        name = '王壹锋'
        name1 = '郑钰婕'
        name2 = '刘洋州'
        name3 = '王静岚'
        movies = [
            {'title': '星际穿越','year':'2014'},
            {'title': '暗黑', 'year': '2017'},
            {'title': '人生切割术', 'year': '2022'},
            {'title': '流人', 'year': '2022'},
            {'title': '扑克脸', 'year': '2023'},
            {'title': '上传新生', 'year': '2020'},
            {'title': '流氓读书会', 'year': '2025'},
            {'title': '伦敦生活', 'year': '2016'},
            {'title': '星期三', 'year': '2022'},
            {'title': '悬案解码', 'year': '2025'},
            {'title': '人生复本', 'year': '2024'},
        ]
        user = User(name=name,username='Wangyifeng')
        user.set_password('1071816386')
        user1 = User(name=name2,username='Zhengyujie')
        user1.set_password('20020205')
        user2 = User(name=name2,username='Liuyangzhou')
        user2.set_password('12345678')
        user3 = User(name=name2,username='Wangjinglan')
        user3.set_password('696387')
        db.session.add(user)
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        for m in movies:
            movie = Movie(title=m['title'], year=m['year'])
            db.session.add(movie)
        db.session.commit()
        click.echo('Done.')
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
    def admin(username, password):
        """Create user."""
        db.create_all()
        user = db.session.execute(select(User)).scalar()
        if user is not None:
            click.echo('Updating user...')
            user.username = username
            user.set_password(password)  # 设置密码
        else:
            click.echo('Creating user...')
            user = User(username=username, name='Admin')
            user.set_password(password)  # 设置密码
            db.session.add(user)
        db.session.commit()  # 提交数据库会话
        click.echo('Done.')