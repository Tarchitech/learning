from typing import Optional
import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint('price_cents >= 0', name='products_price_cents_check'),
        PrimaryKeyConstraint('id', name='products_pkey'),
        {'schema': 'tony'}
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)

    order_items: Mapped[list['OrderItems']] = relationship('OrderItems', back_populates='product')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        {'schema': 'tony'}
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    orders: Mapped[list['Orders']] = relationship('Orders', back_populates='user')


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        CheckConstraint("status = ANY (ARRAY['pending'::text, 'paid'::text, 'shipped'::text, 'cancelled'::text])", name='orders_status_check'),
        ForeignKeyConstraint(['user_id'], ['tony.users.id'], name='orders_user_id_fkey'),
        PrimaryKeyConstraint('id', name='orders_pkey'),
        Index('idx_orders_user_id', 'user_id'),
        {'schema': 'tony'}
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    user: Mapped['Users'] = relationship('Users', back_populates='orders')
    order_items: Mapped[list['OrderItems']] = relationship('OrderItems', back_populates='order')


class OrderItems(Base):
    __tablename__ = 'order_items'
    __table_args__ = (
        CheckConstraint('quantity > 0', name='order_items_quantity_check'),
        ForeignKeyConstraint(['order_id'], ['tony.orders.id'], name='order_items_order_id_fkey'),
        ForeignKeyConstraint(['product_id'], ['tony.products.id'], name='order_items_product_id_fkey'),
        PrimaryKeyConstraint('id', name='order_items_pkey'),
        Index('idx_order_items_order_id', 'order_id'),
        {'schema': 'tony'}
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_cents_at_purchase: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped['Orders'] = relationship('Orders', back_populates='order_items')
    product: Mapped['Products'] = relationship('Products', back_populates='order_items')
