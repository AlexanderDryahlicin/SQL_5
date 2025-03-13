from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship('Book', back_populates='publisher')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    publisher = relationship('Publisher', back_populates='books')
    sales = relationship('Sale', back_populates='book')

class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sales = relationship('Sale', back_populates='shop')

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    shop_id = Column(Integer, ForeignKey('shops.id'))
    sale_date = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)  # Стоимость покупки
    book = relationship('Book', back_populates='sales')
    shop = relationship('Shop', back_populates='sales')

