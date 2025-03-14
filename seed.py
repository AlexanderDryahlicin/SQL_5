from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base, Publisher, Book, Shop, Sale
from datetime import datetime
import os
from dotenv import load_dotenv
# Загружаем переменные окружения из файла .env
load_dotenv()

# Параметры подключения к базе данных
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Подключение к базе данных PostgreSQL
DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

def seed_data():
    # Удаляем все таблицы с использованием CASCADE
    with engine.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS sales CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS stocks CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS book_shop CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS books CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS shops CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS publishers CASCADE;"))
        connection.commit()
    print("Все таблицы удалены с использованием CASCADE.")

    # Создаём все таблицы заново
    Base.metadata.create_all(engine)
    print("Все таблицы созданы заново.")

    # Добавляем издателей
    publisher1 = Publisher(name="Пушкин")
    publisher2 = Publisher(name="Достоевский")
    publisher3 = Publisher(name="Толстой")

    session.add_all([publisher1, publisher2, publisher3])
    session.commit()
    print("Издатели добавлены.")

    # Добавляем книги
    book1 = Book(title="Капитанская дочка", publisher=publisher1)
    book2 = Book(title="Руслан и Людмила", publisher=publisher1)
    book3 = Book(title="Преступление и наказание", publisher=publisher2)
    book4 = Book(title="Война и мир", publisher=publisher3)

    session.add_all([book1, book2, book3, book4])
    session.commit()
    print("Книги добавлены.")

    # Добавляем магазины
    shop1 = Shop(name="Буквоед")
    shop2 = Shop(name="Лабиринт")
    shop3 = Shop(name="Книжный дом")

    session.add_all([shop1, shop2, shop3])
    session.commit()
    print("Магазины добавлены.")

    # Добавляем продажи
    sale1 = Sale(book=book1, shop=shop1, price=600, sale_date=datetime(2022, 11, 9))
    sale2 = Sale(book=book2, shop=shop1, price=500, sale_date=datetime(2022, 11, 8))
    sale3 = Sale(book=book1, shop=shop2, price=580, sale_date=datetime(2022, 11, 5))
    sale4 = Sale(book=book4, shop=shop3, price=490, sale_date=datetime(2022, 11, 2))
    sale5 = Sale(book=book1, shop=shop1, price=600, sale_date=datetime(2022, 10, 26))

    session.add_all([sale1, sale2, sale3, sale4, sale5])
    session.commit()
    print("Продажи добавлены.")

    print("Тестовые данные успешно добавлены в базу данных!")

if __name__ == "__main__":
    seed_data()