import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

from models import create_tables, Publisher, Book, Shop, Stock, Sale

# DSN = 'postgresql://postgres:1234@localhost:5432/work6'
DSN = os.getenv("DSN")

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

try:
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
except:
    print('Все или часть данных уже были загружены в базу данных!')

session.close()

def main():
    try:
        id = int(input('Введите id издателя (число),которого необходимо найти или нажмите Enter для поиска по имени: '))
        if id:
            requests_publisher(id=id)
    except:
        name = input('Введите имя издателя, которого необходимо найти: ')
        requests_publisher(name=name)


def requests_publisher(id=None, name=None):
    if id:
        query = session.query(Publisher, Shop).filter(Publisher.id == id)
        query = query.join(Book, Book.id_publisher == Publisher.id)
        query = query.join(Stock, Stock.id_book == Book.id)
        query = query.join(Shop, Stock.id_shop == Shop.id)
        records = query.all()
        for publisher, shop in records:
            print(f'Книги издателя "{publisher.name}" продаются в магазине: "{shop.name}"')
        if records is None:
            print('Издатель не найден в базе данных')

    elif name:

        query = session.query(Publisher, Shop).filter(Publisher.name == name)
        query = query.join(Book, Book.id_publisher == Publisher.id)
        query = query.join(Stock, Stock.id_book == Book.id)
        query = query.join(Shop, Stock.id_shop == Shop.id)
        records = query.all()
        for publisher, shop in records:
            print(f'Книги издателя "{publisher.name}" продаются в магазине: "{shop.name}"')
        if records is None:
            print('Издатель не найден в базе данных')
    else:
        print('Не введены данные для поиска в базе данных')

main()


