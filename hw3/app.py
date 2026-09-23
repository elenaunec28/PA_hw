from decimal import Decimal
from typing import Optional

from sqlalchemy import create_engine, String, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker




class Base(DeclarativeBase):
    pass


engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name!r}, price={self.price})>"


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(255))
    products: Mapped[list["Product"]] = relationship(back_populates='category')

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name!r})>"


Base.metadata.create_all(engine)


if __name__ == '__main__':
    laptop = Product(name='Ноутбук', price=59999.99,
                     category=Category(name='Электроника'))
    session.add(laptop)
    session.commit()

    print(laptop, laptop.category.name)