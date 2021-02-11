from flask import Blueprint, render_template, redirect, url_for, flash  
from flask_login import login_required
from delivery.ext.login.form import CategoryForm, ItemsForm
from delivery.ext.login.controller import create_category, create_item

category = Blueprint("cate", __name__)

@category.route('/')
@category.route('/page')
@login_required
def page():
    return render_template('login.html')


@category.route('/categoria', methods=['GET', 'POST'])
@login_required
def register_category():
    cate = CategoryForm()

    if cate.validate_on_submit():  
        try:
            create_category(
                name=cate.name.data,
            )
            flash('Categoria registrada com sucesso!', 'success')
            return redirect(url_for('.register_category'))
        except Exception:
            flash('Essa categoria já existe, registre outra!', 'warning')
            return redirect(url_for('.register_category'))

    return render_template("categoria.html", cate=cate)


@category.route('/store', methods=['GET', 'POST'])
@login_required
def register_store():
    pass


@category.route('/items', methods=['GET', 'POST'])
@login_required
def register_items():
    item = ItemsForm()

    if item.validate_on_submit():  
        create_item(
            name=item.name.data,
            image=item.image.data,
            price=item.price.data,
            store_id=item.store_id.data,
            manysold=item.manysold.data,
            dateadded=item.dateadded.data
        )
        flash('Item registrado com sucesso!', 'success')
        return redirect(url_for('.register_items'))

    return render_template("items.html", item=item)
