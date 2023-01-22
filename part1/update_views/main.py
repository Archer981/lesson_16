# Имеется наполненная БД с таблицей guide и полуготовый код на фласке.
# Напишите представления для следующих ендпоинтов:
#
# Method: GET
# URL: /guides
# Response: [{guide_json}, {guide_json}, {guide_json}]
#
# Method: GET
# URL: /guides/1
# Response: { <guide_json> }
#
#
from flask import Flask, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from guides_sql import CREATE_TABLE, INSERT_VALUES

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


@app.route('/')
def main_page():
    return 'Главная страница'


@app.route("/guides")
def get_guides():
    # TODO допишите представления
    records = db.session.query(Guide).all()
    result = []
    for record in records:
        result.append({
            'id': record.id,
            'surname': record.surname,
            'full_name': record.full_name,
            'tours_count': record.tours_count,
            'bio': record.bio,
            'is_pro': record.is_pro,
            'company': record.company
        })
    return jsonify(result)


@app.route("/guides/<int:gid>")
def get_guide(gid):
    # TODO допишите представления
    record = db.session.query(Guide).get(gid)
    result = {
        'id': record.id,
        'surname': record.surname,
        'full_name': record.full_name,
        'tours_count': record.tours_count,
        'bio': record.bio,
        'is_pro': record.is_pro,
        'company': record.company
    }
    return jsonify(result)

# чтобы увидеть результат работы функций
# запустите фаил и
# перейдите по адресу:
# 127.0.0.1:5000/guides
# 127.0.0.1:5000/guides/1


if __name__ == "__main__":
    app.run()
