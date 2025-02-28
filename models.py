from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

db = SQLAlchemy()

def generate_uuid():
    return str(uuid4())

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True, nullable=False)
    username = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    total_price = db.Column(db.Numeric(10,2), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    order_item_id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True, nullable=False)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Numeric(10,2), nullable=False)
