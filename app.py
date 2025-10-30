from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from pathlib import Path
import click


app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(Path(app.root_path)/'data.db') 

db = SQLAlchemy(app, model_class=Base)

class User(db.Model):
    __tablename__ = 'user'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(20))

class Movie(db.Model):
    __tablename__='movie'
    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(String(60))
    year:Mapped[str] = mapped_column(String(4))


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
    name = 'Wang Yifeng'
    movies = [
        {'title':'星际穿越','year':'2013'},
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

'''
@app.route('/')
def home():
    return render_template('index.html', name=name, movies=movies)
'''

@app.route('/')
def index():
    user = db.session.execute(select(User)).scalar()
    movies = db.session.execute(select(Movie)).scalars().all()
    return render_template('index.html',user=user,movies=movies)


if __name__ == '__main__':
    app.run(debug=True)