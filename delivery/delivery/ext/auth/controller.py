import os, click
import cv2
import numpy as np
import warnings

from flask import redirect, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask import current_app as app
from delivery.ext.db.models import User, Category, Store, Items, Address, Order
from delivery.ext.db import db, models



ALG = "pbkdf2:sha256"

def del_category(self, id):
    category = Category.id
    db.session.delete(category)
    db.session.commit()


def list_users():
    """Lista de usuários registrados"""
    users = models.User.query.all()
    click.echo(f"Lista de usuarios {users}")

def list_categorys():
    """Lista de categorias registradas"""
    categorys = models.Category.query.all()
    click.echo(f"Lista de categoria {categorys}")

def list_stores():
    """Lista de lojas"""
    stores = models.Store.query.all()
    click.echo(f"Lista de lojas {stores}")

def list_itens():
    """Lista de itens registrados"""
    items = models.Items.query.all()
    click.echo(f"Lista de itens {items}")

def list_address():
    """Lista de endereços registrados"""
    address = models.Address.query.all()
    click.echo(f"Lista de endereços com CEP {address}")

def list_order():
    """Lista de ordem de compras"""
    order = models.Order.query.all()
    click.echo(f"Lista de ordem de compras {order}")

def create_user(name: str, email: str, password: str, admin:bool = False) -> User:
    user = User(
        name = name,
        email = email,
        password = generate_password_hash(password, ALG),
        admin = admin
    )
    db.session.add(user)
    db.session.commit()
    return user
    
def create_category(name: str, on_menu: bool) -> Category:
    category = Category(
        name = name,
        on_menu = on_menu
    )
    db.session.add(category)
    db.session.commit()
    return category

def create_store(name_store: str, user_id: int, category_id:str , active: bool) -> Store:
    store = Store(
        name_store = name_store,
        user_id = user_id,
        category_id = category_id,
        active = active
    )
    db.session.add(store)
    db.session.commit()
    return store

def create_item(name: str, price: float, store_id: str, available: bool=True) -> Items:
    items = Items(
        name = name,
        price = price,
        store_id = store_id,
        available = available,
    )
    db.session.add(items)
    db.session.commit()
    return items

def create_address(zip_code: str, state: str, city: str, address: str, number_house: int, user_id: str) -> Address:
    address = Address(
        zip_code = zip_code,
        state = state,
        city = city,
        address = address,
        number_house = number_house,
        user_id = user_id
    )
    db.session.add(address)
    db.session.commit()
    return address

def create_order(created_at: str, completed: bool, user_id: str, store_id: str) -> Order:
    order = Order(
        created_at = created_at,
        completed = completed,
        user_id = user_id,
        store_id = store_id,
    )
    db.session.add(order)
    db.session.commit()
    return order

"""
def save_item_picture(filename, filestore):
    filename = os.path.join(
        app.config["UPLOAD_FOLDER"],
        secure_filename(filename)
    )
    filestore.save(filename)
"""
def save_user_picture(filename, filestore):
    filename = os.path.join(
        app.config["UPLOAD_FOLDER"],
        secure_filename(filename)
    )
    filestore.save(filename)
    #imgresizer(filename) this will decrease image
    #TODO: 
    #1) Verificar se o diretório existe.
    #2) criar o diretório se não existir

def imgresizer(path):
    img = cv2.imread(path)
    img = cv2.resize(img,(128,128))
    path = path[0:-4]
    cv2.imwrite(path+"_reduced.png",img)
# Use nesta funcao o parametro caminho absoluto
#ex: imgresizer("C:/Users/e-ron/code/Web-delivery/delivery/uploads/teste.jpg")