from decimal import Decimal
from typing import List, Optional

from sqlalchemy import create_engine, String, Numeric, ForeignKey, func
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column,
                            relationship, sessionmaker)

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(255))

    products: Mapped[List["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category: Mapped["Category"] = relationship(back_populates="products")


Base.metadata.create_all(engine)

electronics = Category(name="Электроника", description="Гаджеты и устройства.")
books = Category(name="Книги", description="Печатные книги и электронные книги.")
clothes = Category(name="Одежда", description="Одежда для мужчин и женщин.")
session.add_all([electronics, books, clothes])

session.add_all([
    Product(name="Смартфон", price=299.99, in_stock=True, category=electronics),
    Product(name="Ноутбук", price=499.99, in_stock=True, category=electronics),
    Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=books),
    Product(name="Джинсы", price=40.50, in_stock=True, category=clothes),
    Product(name="Футболка", price=20.00, in_stock=True, category=clothes),
])
session.commit()

#Задача 2: Чтение данных
print("Задача 2: категории и их продукты")
categories = session.query(Category).all()
for category in categories:
    print(f"{category.name} — {category.description}")
    for product in category.products:
        print(f"{product.name}: {product.price}")
print()

#Задача 3: Обновление данных
smartphone = session.query(Product).filter(Product.name == "Смартфон").first()
if smartphone:
    smartphone.price = 349.99
    session.commit()
    print(f"Задача 3: новая цена '{smartphone.name}': {smartphone.price}\n")
else:
    print("Задача 3: продукт 'Смартфон' не найден\n")

#Задача 4: Агрегация и группировка
print("Задача 4: количество продуктов в каждой категории")
products_per_category = session.query(
    Category.name,
    func.count(Product.id).label('product_count')
).outerjoin(Product).group_by(Category.id, Category.name).all()
for row in products_per_category:
    print(f"{row.name}: {row.product_count}")
print()

#Задача 5: Группировка с фильтрацией
print("Задача 5: категории, где больше одного продукта")
big_categories = session.query(
    Category.name,
    func.count(Product.id).label('product_count')
).join(Product).group_by(Category.id, Category.name) \
 .having(func.count(Product.id) > 1).all()
for row in big_categories:
    print(f"{row.name}: {row.product_count}")