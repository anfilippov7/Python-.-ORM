import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = 'postgresql://postgres:1234@localhost:5432/work6'

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
        q = session.query(Publisher).filter(Publisher.id == id)
        for s in q.all():
            print('Данные издателя: ', s.id, s.name)
    elif name:
        q = session.query(Publisher).filter(Publisher.name == name)
        for s in q.all():
                print('Данные издателя: ', s.id, s.name)
    else:
        print('Не введены данные для поиска в базе данных')

main()

