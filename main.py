from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Publisher, Book, Shop, Sale

# Подключение к базе данных PostgreSQL
DSN = 'postgresql://postgres:Haligali1982@localhost:5432/test44'
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

def get_sales_by_publisher():
    # Запрос имени или идентификатора издателя
    publisher_input = input("Введите имя или идентификатор издателя: ")

    try:
        # Пытаемся преобразовать ввод в число (если введен идентификатор)
        publisher_id = int(publisher_input)
        publisher = session.query(Publisher).filter(Publisher.id == publisher_id).first()
    except ValueError:
        # Если ввод не число, ищем по имени
        publisher = session.query(Publisher).filter(Publisher.name.ilike(f'%{publisher_input}%')).first()

    if not publisher:
        print("Издатель не найден.")
    else:
        # Выполняем запрос для выборки данных
        results = (
            session.query(Book.title, Shop.name, Sale.price, Sale.sale_date)
            .join(Sale, Sale.book_id == Book.id)
            .join(Shop, Sale.shop_id == Shop.id)
            .filter(Book.publisher_id == publisher.id)
            .order_by(Sale.sale_date.desc())
            .all()
        )

        # Выводим результаты
        if results:
            print(f"Книги издателя '{publisher.name}':")
            for title, shop_name, price, sale_date in results:
                print(f"{title} | {shop_name} | {price} | {sale_date.strftime('%d-%m-%Y')}")
        else:
            print(f"Нет данных о продажах книг издателя '{publisher.name}'.")

if __name__ == "__main__":
    get_sales_by_publisher()