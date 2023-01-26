# УРОК 16 Задание 8
# В этом финальном задании вам нужно
# применить знания о моделях для создания 3 представлений,
# которые реализуют запросы на создание, добавление, удаление.

"""
    # Задание
    # Шаг 1.
    # ######
    # Создайте представение для эндпоинта GET /guides
    # которое возвращает список всех гидов со всеми полями
    # в формате JSON
    #
    #
    # Шаг 2.
    # ######
    # - Создайте представение для эндпоинта GET /guides/{id}
    # которое возвращает одного гида со всеми полями
    # в формате JSON в соответствии с его id
    #
    # Шаг 3.
    # ######
    # Создайте представение для эндпоинта
    # GET /guides/{id}/delete`, которое удаляет
    # одного гида в соответствии с его `id`
    #
    # Шаг 4.
    # ######
    # Создайте представление для эндпоинта POST /guides
    #  которое добавляет в базу данных гида, при получении
    # следующих данных:
    # {
    #     "surname": "Иванов",
    #     "full_name": "Иван Иванов",
    #     "tours_count": 7,
    #     "bio": "Провожу экскурсии",
    #     "is_pro": true,
    #     "company": "Удивительные экскурсии"
    # }
    # Шаг 5.
    # ######
    # - Допишите представление из шага 1 для фильтрации так,
    # чтобы при получении запроса типа /guides?tours_count=1
    # возвращались гиды с нужным количеством туров.
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from guides_sql import CREATE_TABLE, INSERT_VALUES


def convert_to_dict(convert):
    return {
        "id": convert.id,
        "surname": convert.surname,
        "full_name": convert.full_name,
        "tours_count": convert.tours_count,
        "bio": convert.bio,
        "is_pro": convert.is_pro,
        "company": convert.company
    }


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)
with db.session.begin():
    db.session.execute(text(CREATE_TABLE))
    db.session.execute(text(INSERT_VALUES))


class Guide(db.Model):
    __tablename__ = 'guide'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String)
    full_name = db.Column(db.String)
    tours_count = db.Column(db.Integer)
    bio = db.Column(db.String)
    is_pro = db.Column(db.Boolean)
    company = db.Column(db.Integer)

# TODO напишите роуты здесь


@app.get('/')
def main_page():
    return 'Главная страница'


@app.route('/guides', methods=['POST', 'GET'])
def all_guides_page():
    if request.method == 'POST':
        new_guide = Guide(
        surname=request.form.get('surname'),
        full_name=request.form.get('full_name'),
        tours_count=request.form.get('tours_count'),
        bio=request.form.get('bio'),
        is_pro=request.form.get('is_pro'),
        company=request.form.get('company')
        )
        db.session.add(new_guide)
        db.commit()
        return 'Новый гид добавлен'
    tours_count = request.args.get('tours_count')
    result = []
    if tours_count:
        for guide in db.session.query(Guide).filter(Guide.tours_count == tours_count).all():
            result.append(convert_to_dict(guide))
    else:
        for guide in db.session.query(Guide).all():
            result.append(convert_to_dict(guide))
    return jsonify(result)


@app.get('/guides/<int:id>')
def guide_page(id):
    return jsonify(convert_to_dict(db.session.query(Guide).get(id)))


@app.get('/guides/<int:id>/delete')
def guide_delete(id):
    db.session.query(Guide).filter(Guide.id == id).delete()
    db.session.commit()
    return 'Удалено'


if __name__ == "__main__":
    app.run()
