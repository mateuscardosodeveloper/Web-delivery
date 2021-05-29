import os
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, \
    flash, request, send_from_directory
from flask import current_app as app
from flask_login import login_required, current_user

from delivery.ext.auth.form import CategoryForm, CategoryEditForm, \
    ItemsForm, ItemsEditForm, StoresForm, StoreEditForm, AddressForm,\
    AddressEditForm, OrderForm, OrderEditForm, OrderItemsForm
from delivery.ext.auth.controller import create_category, create_item,\
    create_store, create_address, create_order, save_user_picture, list_image, delete_image
from delivery.ext.db import db
from delivery.ext.db.models import Category, Store, Items, Address, Order, OrderItems
from werkzeug.utils import secure_filename


category = Blueprint("cate", __name__)


@category.route('/')
@category.route('/page')
@login_required
def page():
    return render_template('login.html')


@category.route('/lista_categoria', methods=['GET', 'POST'])
@login_required
def list_category():
    categorys = Category.query.all()
    return render_template('category/list_category.html', categorys=categorys)


@category.route('/categoria', methods=['GET', 'POST'])
@login_required
def register_category():
    form = CategoryForm()

    if form.validate_on_submit():
        try:
            create_category(
                name=form.name.data,
                on_menu=form.on_menu.data
            )
            flash('Categoria registrada com sucesso!', 'success')
            return redirect(url_for('.register_category'))
        except Exception:
            flash('Essa categoria já existe, registre outra!', 'warning')
            return redirect(url_for('.register_category'))

    return render_template("category/register_category.html", form=form)


@category.route('/editar_categoria/<id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    form = CategoryEditForm()
    category = Category.query.filter_by(id=id).first()

    if form.validate_on_submit():
        category.name = form.name.data
        category.on_menu = form.on_menu.data

        try:
            db.session.add(category)
            db.session.commit()
            flash('Alterado com sucesso', 'success')
            return redirect(url_for('.list_category'))
        except Exception:
            db.session.rollback()
            flash('Houve algum erro ao editar', 'danger')
            return redirect(url_for('.list_category'))

    form.name.data = category.name
    form.on_menu.data = category.on_menu
    return render_template('category/edit_category.html', category=category, form=form)


@category.route('/deletar_categoria/<id>')
@login_required
def delete_category(id):
    category = Category.query.filter_by(id=id).first()
    db.session.delete(category)
    db.session.commit()
    flash('Categoria deletada!', 'success')
    return redirect(url_for('.list_category'))


@category.route('/lista_loja', methods=['GET', 'POST'])
@login_required
def list_store():
    stores = Store.query.all()
    return render_template('store/list_store.html', stores=stores)


@category.route('/deletar_loja/<id>')
@login_required
def delete_store(id):
    store = Store.query.filter_by(id=id).first()
    db.session.delete(store)
    db.session.commit()
    flash('Estabelecimento deletado!', 'success')
    return redirect(url_for('.list_store'))


@category.route('/editar_loja/<id>', methods=['GET', 'POST'])
@login_required
def edit_store(id):
    form = StoreEditForm()
    store = Store.query.filter_by(id=id).first()

    if form.validate_on_submit():
        store.name_store = form.name_store.data
        if form.category_id.data == None:
            pass
        else:
            store.category_id = form.category_id.data.name
        if form.user_id.data == None:
            pass
        else:
            store.user_id = form.user_id.data.email
        store.active = form.active.data

        try:
            db.session.add(store)
            db.session.commit()
            flash('Usuario Editado!', 'success')
            return redirect(url_for('.list_store'))
        except Exception:
            db.session.rollback()
            flash('Houve um algum erro ao editar!', 'danger')
            return redirect(url_for('.list_store'))

    form.name_store.data = store.name_store
    form.category_id.data = store.category_id
    form.user_id.data = store.user_id
    form.active.data = store.active
    return render_template('store/edit_store.html', store=store, form=form)


@category.route('/loja', methods=['GET', 'POST'])
@login_required
def register_store():
    form = StoresForm()

    if form.validate_on_submit():
        try:
            create_store(
                name_store=form.name_store.data,
                user_id=current_user.email,
                category_id=form.category_id.data.name,
                active=form.active.data
            )
            flash('Estabelecimento registrado com sucesso!', 'success')
            return redirect(url_for('.register_store'))
        except Exception:
            flash('Esse estabelecimento já foi registrado. Cadastre outro!', 'warning')
            return redirect(url_for('.register_store'))

    return render_template("store/register_store.html", form=form)


@category.route('/lista_itens', methods=['GET', 'POST'])
@login_required
def list_items():
    item = Items.query.all()
    return render_template('items/list_items.html', item=item)


@category.route('/editar_itens/<id>', methods=['GET', 'POST'])
@login_required
def edit_items(id):
    form = ItemsEditForm()
    items = Items.query.filter_by(id=id).first()
    nome_arquivo = list_image(id)

    if form.validate_on_submit():
        items.name = form.name.data
        items.price = form.price.data
        items.description = form.description.data
        if form.store_id.data == None:
            pass
        else:
            items.store_id = form.store_id.data.name_store
        items.available = form.available.data

        try:
            image = request.files['image']
            upload_folder = os.path.join(app.config["UPLOAD_FOLDER"])
            secure_filename(upload_folder)
            delete_image(id)
            image.save(f'{upload_folder}/{items.id}.jpg')
            db.session.add(items)
            db.session.commit()
            flash('Item editado com sucesso', 'success')
            return redirect(url_for('.list_items'))
        except Exception:
            db.session.rollback()
            flash('Houve algum erro ao editar o item', 'danger')
            return redirect(url_for('.list_items'))

    form.name.data = items.name
    form.price.data = items.price
    form.description.data = items.description
    form.store_id.data = items.store_id
    form.available.data = items.available
    return render_template('items/edit_items.html', items=items, form=form, capa_item=nome_arquivo)


@category.route('/deletar_itens/<id>')
@login_required
def delete_items(id):
    delete_image(id)
    items = Items.query.filter_by(id=id).first()
    db.session.delete(items)
    db.session.commit()
    flash('Item deletado!', 'success')
    return redirect(url_for('.list_items'))


@category.route('/items', methods=['GET', 'POST'])
@login_required
def register_items():
    form = ItemsForm()

    if form.validate_on_submit():
        try:
            items = create_item(
                name=form.name.data,
                price=form.price.data,
                description=form.description.data,
                store_id=form.store_id.data.name_store,
                available=form.available.data,
            )
            image = request.files['image']
            upload_folder = os.path.join(app.config["UPLOAD_FOLDER"])
            secure_filename(upload_folder)
            image.save(f'{upload_folder}/{items.id}.jpg')

            flash('Item registrado com sucesso!', 'success')
            return redirect(url_for('.register_items'))
        except Exception:
            flash('Houve algum erro ao cadastrar o item!', 'danger')
            return redirect(url_for('.register_items'))

    return render_template("items/register_items.html", form=form)


@category.route('/lista_endereço', methods=['GET', 'POST'])
@login_required
def list_address():
    addresses = Address.query.all()
    return render_template('address/list_address.html', addresses=addresses)


@category.route('/editar_endereço/<id>', methods=['GET', 'POST'])
@login_required
def edit_address(id):
    form = AddressEditForm()
    address = Address.query.filter_by(id=id).first()

    if form.validate_on_submit():
        address.zip_code = form.zip_code.data
        address.state = form.state.data
        address.city = form.city.data
        address.address = form.address.data
        address.number_house = form.number_house.data

        try:
            db.session.add(address)
            db.session.commit()
            flash('Endereço editado com sucesso!', 'success')
            return redirect(url_for('.list_address'))
        except Exception:
            db.session.rollback()
            flash('Houve algum erro ao editar o endereço', 'danger')
            return redirect(url_for('.list_address'))

    form.zip_code.data = address.zip_code
    form.state.data = address.state
    form.city.data = address.city
    form.address.data = address.address
    form.number_house.data = address.number_house
    return render_template('address/edit_address.html', address=address, form=form)


@category.route('/deletar_endereco/<id>')
@login_required
def delete_address(id):
    address = Address.query.filter_by(id=id).first()
    db.session.delete(address)
    db.session.commit()
    flash('Endereço deletado!', 'success')
    return redirect(url_for('.list_address'))


@category.route('/endereço', methods=['GET', 'POST'])
@login_required
def register_address():
    form = AddressForm()

    if form.validate_on_submit():
        try:
            create_address(
                zip_code=form.zip_code.data,
                state=form.state.data,
                city=form.city.data,
                address=form.address.data,
                number_house=form.number_house.data,
                user_id=current_user.email
            )
            flash('Endereço registrado com sucesso!', 'success')
            return redirect(url_for('.register_address'))
        except Exception:
            flash('Algo deu errado tente novamente!', 'warning')
            return redirect(url_for('.register_address'))

    return render_template("address/register_address.html", form=form)


@category.route('/lista_ordem', methods=['GET', 'POST'])
@login_required
def list_order():
    orders = Order.query.all()
    return render_template('order/list_order.html', orders=orders)


@category.route('/editar_ordem/<id>', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    form = OrderEditForm()
    order = Order.query.filter_by(id=id).first()

    if form.validate_on_submit():
        order.completed = form.completed.data
        if form.store_id.data == None:
            pass
        else:
            order.store_id = form.store_id.data.name_store

        try:
            db.session.add(order)
            db.session.commit()
            flash('Compra editada com sucesso!', 'success')
            return redirect(url_for('.list_order'))
        except Exception:
            db.session.rollback()
            flash('Houve algum erro ao editar a compra', 'danger')
            return redirect(url_for('.list_order'))

    form.completed.data = order.completed
    form.store_id.data = order.store_id
    return render_template('order/edit_order.html', order=order, form=form)


@category.route('/deletar_ordem/<id>')
@login_required
def delete_order(id):
    order = Order.query.filter_by(id=id).first()
    db.session.delete(order)
    db.session.commit()
    flash('Ordem deletada!', 'success')
    return redirect(url_for('.list_order'))


@category.route('/ordem', methods=['GET', 'POST'])
@login_required
def register_order():
    form = OrderForm()

    if form.validate_on_submit():
        try:
            create_order(
                created_at=datetime.now(),
                completed=form.completed.data,
                user_id=current_user.email,
                store_id=form.store_id.data.name_store
            )
            flash('Ordem de compra registrada com sucesso!', 'success')
            return redirect(url_for('.register_order'))
        except Exception:
            flash('Algo deu errado tente novamente!', 'warning')
            return redirect(url_for('.register_order'))

    return render_template("order/register_order.html", form=form)


@category.route('/lista_order_itens', methods=['GET', 'POST'])
@login_required
def list_order_items():
    order_item = OrderItems.query.all()
    return render_template('order_items/list_order_items.html', order_item=order_item)


@category.route('/editar_order_itens', methods=['GET', 'POST'])
@login_required
def edit_order_items():

    return render_template('order_items/edit_order_items.html')


@category.route('/deletar_order_itens', methods=['GET', 'POST'])
@login_required
def delete_order_items():
    pass


@category.route('/ordem_itens', methods=['GET', 'POST'])
@login_required
def register_order_items():
    form = OrderItemsForm()

    return render_template("order_items/register_order_items.html", form=form)
