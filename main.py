from flask import Flask, request, render_template
from parser_hh import parser_hh
from parser_rocada import parser_roc
import sqlite3 as sq

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'


@app.route("/index")
@app.route("/")  # адрес страницы (писать слеш с обеих сторон)
def index():
    # print('hello')
    return render_template('index.html')  # функция рендеринга шаблона - index.html


@app.route("/contacts/")  # адрес страницы (писать слеш с обеих сторон)
def contacts():
    tel_developer = '+79603723033'
    developer_name = 'Aleksey'
    adress_developer = 'Ulyanovsk'
    return render_template('contacts.html', name=developer_name, my_adress=adress_developer,
                           tel=tel_developer)  # функция рендеринга шаблона - contacts.html
    # name=developer_name - передача контекста(данных) из контроллера


def about():
    return render_template('about.html')


@app.route('/results/')  # адрес страницы (писать слеш с обеих сторон)
def results():
    with open('result_top_10.txt', 'r') as f:
        parser_data = f.readlines()
    with open('top_10.txt', 'r') as f:
        parser_head = f.readlines()
    with open('city_top_10.txt', 'r') as f:
        city_parser_data = f.readlines()
    with open('city_head_10.txt', 'r') as f:
        city_parser_head = f.readlines()
    return render_template('results.html', parser_data=parser_data, parser_head=parser_head,
                           city_parser_data=city_parser_data, city_parser_head=city_parser_head
                           )


@app.route('/results_SQL/')
def results_sql():
    with open('top_10.txt', 'r') as f:
        parser_head = f.readlines()
    with open('city_head_10.txt', 'r') as f:
        city_parser_head = f.readlines()
    conn = sq.connect('my_base_hh_homeworks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from skills')
    result_skill_SQL = cursor.fetchall()
    cursor.execute('SELECT * from city')
    result_city_SQL = cursor.fetchall()
    conn.close()
    return render_template(
        'results_SQL.html', result_skill_SQL=result_skill_SQL, result_city_SQL=result_city_SQL,
        parser_head=parser_head, city_parser_head=city_parser_head
    )


@app.route('/results_SQLAlchemy/')
def results_SQLAlchemy():
    # establish connections
    engine = create_engine('sqlite:///city_new_test.sqlite', echo=True)
    Base = declarative_base()

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    class SkillTest(Base):
        __tablename__ = 'skill_city_new_test'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        percent = Column(Integer, nullable=True)
        count = Column(Integer, nullable=True)

    class CityTest(Base):
        __tablename__ = 'city_new_test'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        percent = Column(Integer, nullable=True)
        count = Column(Integer, nullable=True)

    with open('top_10.txt', 'r') as f:
        parser_head = f.readlines()
    with open('city_head_10.txt', 'r') as f:
        city_parser_head = f.readlines()

    skills = session.query(SkillTest).all()
    cities = session.query(CityTest).all()

    return render_template(
        'results_SQLAlchemy.html',
        parser_head=parser_head,
        city_parser_head=city_parser_head,
        skills=skills,
        cities=cities
    )


@app.route('/choise/', methods=['GET'])
def choise_get():
    return render_template('choise.html')


@app.route('/choise/', methods=['POST'])
def choise_post():
    text = request.form['proff']
    pages = request.form['pages']
    region = request.form['region']

    if int(pages) < 20:
        info = 'Запрос обработан. Выбор слишком мал, спарсено 20 вакансий'
    elif int(pages) > 2000:
        info = 'Запрос обработан. Выбор слишком велик, спарсено 2000 вакансий.'
    else:
        info = 'Запрос обработан.'

    parser_hh(text, pages, region)
    return render_template('choise.html', info=info)


@app.route('/choise_roc/', methods=['GET'])
def choise_get_roc():
    return render_template('choise_roc.html')


@app.route('/choise_roc/', methods=['POST'])
def choise_post_roc():
    parser_roc()

    with open('history.txt', 'r') as f:
        info = f.readlines()
    return render_template('choise_roc.html', info=info)


if __name__ == "__main__":
    app.run(debug=True)
