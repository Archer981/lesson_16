# Имеется модель и заполненная база данных.
# 1. Напишите функцию get_all() которая будет возвращать все объекты из базы
# 2. Напишите функцию get_one() которая будет принимать аргумент id и
#  возвращать объект из базы, в соответствии с полученным аргументом.
#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import prettytable


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    full_name = db.Column(db.String)
    city = db.Column(db.Integer)
    city_ru = db.Column(db.String)


def get_all():
    # TODO напишите функцию здесь
    pass


def get_one(id):
    # TODO напишите функцию здесь
    pass


# не удаляйте код ниже, он используется для вывода на экран
# результата выполнения составленных вами функций

mytable_one = prettytable.PrettyTable()
mytable_all = prettytable.PrettyTable()
columns = [
    'id', 'email', 'password',
    'full_name', 'city', 'city_ru']
mytable_one.field_names = columns
mytable_all.field_names = columns
rows = [[x.id, x.email, x.password,
         x.full_name, x.city, x.city_ru] for x in get_all()]
obj = get_one(1)
row = [obj.id, obj.email, obj.password,
       obj.full_name, obj.city,
       obj.city_ru]

mytable_all.add_rows(rows)
mytable_one.add_row(row)


if __name__ == "__main__":
    print('get_one:')
    print(mytable_one)
    print('get_all:')
    print(mytable_all)
