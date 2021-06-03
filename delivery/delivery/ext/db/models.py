# -*- encoding: utf-8 -*-
import os
from delivery.ext.db import db, init_app, login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash



@login_manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.Unicode)
    email = db.Column("email", db.Unicode, unique=True)
    password = db.Column("password", db.Unicode)
    admin = db.Column("admin", db.Boolean)

    def get_id(self):
        return str(self.id)

    def auth(self, email: str, password: str) -> bool:
        user = self.query.filter_by(email=email).first()
        if not user:
            return False
        if not check_password_hash(user.password, password):
            return False
        return user
        
    def __repr__(self):
        return self.email


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.Unicode, unique=True)
    on_menu = db.Column("on_menu", db.Boolean)

    def __repr__(self):
        return self.name


class Store(db.Model):
    __tablename__ = "store"
    id = db.Column("id", db.Integer, primary_key=True)
    name_store = db.Column("name_store", db.String, unique=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.email"))
    category_id = db.Column("category_id", db.Integer, db.ForeignKey("category.name"))
    active = db.Column("active", db.Boolean, default=False)

    user = db.relationship("User", foreign_keys=user_id)
    category = db.relationship("Category", foreign_keys=category_id)

    def __repr__(self):
        return self.name_store


class Items(db.Model):
    __tablename__ = "items"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.Unicode)
    quantity = db.Column("quantity", db.Integer)
    price = db.Column("price", db.Float(asdecimal=True, decimal_return_scale=2))
    description = db.Column("description", db.Text(length=None))
    store_id = db.Column("store_id", db.Integer, db.ForeignKey("store.name_store"))
    available = db.Column("available", db.Boolean)
    
    store = db.relationship("Store", foreign_keys=store_id)

    def __repr__(self):
        return self.name


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column("id", db.Integer, primary_key=True)
    created_at = db.Column("created_at", db.DateTime)
    completed = db.Column("completed", db.Boolean)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.email"))
    store_id = db.Column("store_id", db.Integer, db.ForeignKey("store.name_store"))
    address_id = db.Column("address_id", db.Integer, db.ForeignKey("address.zip_code"))
    
    user = db.relationship("User", foreign_keys=user_id)
    store = db.relationship("Store", foreign_keys=store_id)
    address = db.relationship("Address", foreign_keys=address_id)


    def __repr__(self):
        return f'{self.user_id} {self.created_at}'

class OrderItems(db.Model):
    __tablename__ = "order_items"
    order_id = db.Column("order_id", db.Integer, db.ForeignKey("order.created_at"))
    items_id = db.Column("items_id", db.Integer, db.ForeignKey("items.name"))
    quant = db.Column("quant", db.Integer)
    id = db.Column("id", db.Integer, primary_key=True)

    order = db.relationship("Order", foreign_keys=order_id)
    items = db.relationship("Items", foreign_keys=items_id)


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column("id", db.Integer, primary_key=True)
    zip_code = db.Column("zip_code", db.Unicode)
    state = db.Column("country", db.Unicode)
    city = db.Column("city", db.Unicode)
    address = db.Column("address", db.Unicode)
    number_house = db.Column("number_house", db.Unicode)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.email"))

    user = db.relationship("User", foreign_keys=user_id)

    def __repr__(self):
        return self.zip_code


class Checkout(db.Model):
    __tablename__ = "checkout"
    id = db.Column("id", db.Integer, primary_key=True)
    payment = db.Column("payment", db.Unicode)
    total = db.Column("total", db.Numeric)
    created_at = db.Column("created_at", db.DateTime)
    completed = db.Column("completed", db.Boolean)
    order_id = db.Column("order_id", db.Integer, db.ForeignKey("order.created_at"))

    order = db.relationship("Order", foreign_keys=order_id)